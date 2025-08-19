from collections.abc import Generator
import re
from typing import Any, Dict, List, Optional, Tuple
import traceback
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# Import the enhanced tool for Bilibili API operations
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
from bilibili_enhanced_tool import BilibiliEnhancedTool

# Set up logger with custom handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


class BilibiliSubtitlePluginTool(Tool):
    """
    哔哩哔哩字幕提取工具
    """

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Extract subtitles from Bilibili videos using BilibiliEnhancedTool

        Args:
            tool_parameters: Dictionary containing tool input parameters:
                - video_id (str): Bilibili video ID (BV number or AV number)

        Yields:
            ToolInvokeMessage: Message containing the extracted subtitle content

        Raises:
            Exception: If subtitle extraction fails, an exception with error information is thrown
        """
        # 1. Get credentials from runtime
        try:
            logger.info("Retrieving Bilibili credentials")
            sessdata = self.runtime.credentials["sessdata"]
            bili_jct = self.runtime.credentials["bili_jct"]
            buvid3 = self.runtime.credentials["buvid3"]
            logger.info("Bilibili credentials retrieved successfully")
        except KeyError as e:
            logger.error(f"Failed to get credentials: {str(e)}")
            raise Exception("Bilibili credentials not configured or invalid. Please provide SESSDATA, BILI_JCT and BUVID3 in plugin settings.")

        # 2. Get tool input parameters
        logger.info("Getting tool input parameters")
        video_id = tool_parameters.get("video_id", "")
        logger.info(f"Video ID: {video_id}")

        if not video_id:
            logger.error("Video ID is empty")
            raise Exception("Video ID cannot be empty.")

        # 3. Validate and normalize video ID
        logger.info("Validating and normalizing video ID")
        video_id = self._normalize_video_id(video_id)
        if not video_id:
            logger.error(f"Invalid video ID format: {tool_parameters.get('video_id', '')}")
            raise Exception(f"Invalid video ID format. Please provide a valid BV number (e.g., 'BV1GJ411x7h7') or AV number (e.g., 'av170001' or '170001').")
        logger.info(f"Normalized video ID: {video_id}")

        # 4. Use BilibiliEnhancedTool to get subtitles
        try:
            # Initialize the enhanced tool with credentials
            logger.info("Initializing BilibiliEnhancedTool")
            enhanced_tool = BilibiliEnhancedTool(sessdata, bili_jct, buvid3)
            
            # Get video information
            logger.info("Getting video information")
            video_info = enhanced_tool.get_video_info(video_id)
            if not video_info:
                logger.error(f"Failed to get video information for {video_id}")
                raise Exception(f"Failed to get video information for {video_id}")
            
            video_title = video_info.get('title', 'Unknown Title')
            video_author = video_info.get('owner', {}).get('name', 'Unknown Author')
            logger.info(f"Video info: title='{video_title}', author='{video_author}'")
            
            # Get subtitle text using the enhanced tool
            logger.info("Getting video subtitle")
            subtitle_text = enhanced_tool.get_video_subtitle(video_id)
            
            if not subtitle_text:
                logger.warning(f"No available subtitles found for video '{video_title}'")
                raise Exception(f"Video '{video_title}' has no available subtitles.")
            
            # Get subtitle info to determine language
            pages = enhanced_tool.get_video_pages(video_id)
            if pages and len(pages) > 0:
                cid = pages[0].get('cid')
                subtitle_info = enhanced_tool.get_subtitle_info(video_id, cid)
                subtitle_language = "Unknown Language"
                if subtitle_info and len(subtitle_info) > 0:
                    subtitle_language = subtitle_info[0].get('lan_doc', 'Unknown Language')
            else:
                subtitle_language = "Unknown Language"
            
            logger.info(f"Subtitle content processed: {len(subtitle_text)} characters")
            
            # Return result using variable messages for declared output schema
            logger.info("Preparing subtitle results for response")
            logger.info(f"Subtitles successfully retrieved for video '{video_title}'")
            
            # Return each declared output variable separately
            yield self.create_variable_message("subtitles", subtitle_text)
            yield self.create_variable_message("video_title", video_title)
            yield self.create_variable_message("video_author", video_author)
            yield self.create_variable_message("subtitle_language", subtitle_language)
            
            # Also provide a summary text message for user
            summary_text = f"Successfully extracted subtitles from video '{video_title}' by {video_author}. Language: {subtitle_language}. Subtitle length: {len(subtitle_text)} characters."
            yield self.create_text_message(summary_text)
            
        except Exception as e:
            import traceback
            error_type = type(e).__name__
            error_msg = str(e)
            error_traceback = traceback.format_exc()
            
            # Log detailed exception information
            logger.error(f"Failed to get subtitles: {error_type} - {error_msg}")
            logger.error(f"Exception traceback: \n{error_traceback}")
            
            # Return empty output variables for declared output schema
            yield self.create_variable_message("subtitles", "")
            yield self.create_variable_message("video_title", "")
            yield self.create_variable_message("video_author", "")
            yield self.create_variable_message("subtitle_language", "")
            
            # Return error message to user
            yield self.create_text_message(f"Failed to get subtitles: {error_type} - {error_msg}")

    def _normalize_video_id(self, video_id: str) -> str:
        """
        Validate and normalize video ID format
        
        Args:
            video_id: Video ID input (BV number, AV number, or just number)
            
        Returns:
            Normalized video ID (BV or av format), empty string if invalid
        """
        logger.info(f"Normalizing video ID: {video_id}")
        
        # Remove whitespace
        video_id = video_id.strip()
        
        # Check if it's a BV number
        bv_pattern = r'^BV([a-zA-Z0-9]{10})$'
        bv_match = re.match(bv_pattern, video_id)
        if bv_match:
            logger.info(f"Valid BV number: {video_id}")
            return video_id
            
        # Check if it's an AV number with 'av' prefix
        av_pattern = r'^av([0-9]+)$'
        av_match = re.match(av_pattern, video_id)
        if av_match:
            logger.info(f"Valid AV number: {video_id}")
            return video_id
            
        # Check if it's just a number (treat as AV number)
        number_pattern = r'^([0-9]+)$'
        number_match = re.match(number_pattern, video_id)
        if number_match:
            normalized_id = f"av{video_id}"
            logger.info(f"Normalized number to AV format: {normalized_id}")
            return normalized_id
        
        logger.warning(f"Invalid video ID format: {video_id}")
        return ""