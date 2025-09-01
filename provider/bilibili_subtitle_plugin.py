from typing import Any
import httpx
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


class BilibiliSubtitlePluginProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate Bilibili credentials
        
        Args:
            credentials: Dictionary containing credential information
            
        Raises:
            ToolProviderCredentialValidationError: When credential validation fails
        """
        logger.info("Starting Bilibili credential validation")
        
        # 1. Extract credential information
        sessdata = credentials.get("sessdata", "")
        bili_jct = credentials.get("bili_jct", "")
        buvid3 = credentials.get("buvid3", "")
        
        # 2. Validate credential completeness
        logger.info("Step 1: Validating credential completeness")
        self._validate_credentials_completeness(sessdata, bili_jct, buvid3)
        logger.info("✓ Credential completeness validation passed")
        
        # 3. Validate credentials via API
        logger.info("Step 2: Validating credentials via API")
        self._validate_credentials_with_api(sessdata, bili_jct, buvid3)
        logger.info("✓ API credential validation passed")
        
        logger.info("Bilibili credential validation completed, all checks passed")
    
    def _validate_credentials_completeness(self, sessdata: str, bili_jct: str, buvid3: str) -> None:
        """Validate credential completeness"""
        if not self._has_sessdata(sessdata):
            logger.error("SESSDATA validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("Missing required credential: SESSDATA. Please ensure all required credential fields are properly configured.")
        
        if not self._has_bili_jct(bili_jct):
            logger.error("bili_jct validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("Missing required credential: bili_jct. Please ensure all required credential fields are properly configured.")
        
        if not self._has_buvid3(buvid3):
            logger.error("buvid3 validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("Missing required credential: buvid3. Please ensure all required credential fields are properly configured.")
    

    
    def _validate_credentials_with_api(self, sessdata: str, bili_jct: str, buvid3: str) -> None:
        """
        Validate credentials via API
        
        Args:
            sessdata: User session data
            bili_jct: CSRF token  
            buvid3: Browser unique identifier
            
        Raises:
            ToolProviderCredentialValidationError: Credential validation failed
        """
        try:
            # Call API to validate credentials
            is_valid = self._check_credentials_with_api(sessdata, bili_jct, buvid3)
            if not is_valid:
                raise ToolProviderCredentialValidationError("Credential validation failed: credentials are invalid or expired. Please check if credentials are correct or try to obtain new ones.")
                
        except ValueError as e:
            # API response related errors (such as login status, error codes, etc.)
            raise ToolProviderCredentialValidationError(f"Credential validation failed: {str(e)}")
            
        except httpx.RequestError as e:
            # Network related errors
            error_msg = str(e)
            if "超时" in error_msg or "timeout" in error_msg.lower():
                raise ToolProviderCredentialValidationError("Credential validation failed: network request timeout, please check network connection and retry")
            elif "连接" in error_msg or "connection" in error_msg.lower():
                raise ToolProviderCredentialValidationError("Credential validation failed: unable to connect to Bilibili server, please check network settings")
            else:
                raise ToolProviderCredentialValidationError(f"Credential validation failed: network request exception - {error_msg}")
                
        except Exception as e:
            # Other unexpected errors
            raise ToolProviderCredentialValidationError(f"Credential validation failed: unknown error occurred - {str(e)}")
    
    def _has_sessdata(self, sessdata: str) -> bool:
        """Check if valid SESSDATA is provided"""
        return sessdata is not None and sessdata.strip() != ""
    
    def _has_bili_jct(self, bili_jct: str) -> bool:
        """Check if valid bili_jct is provided"""
        return bili_jct is not None and bili_jct.strip() != ""
    
    def _has_buvid3(self, buvid3: str) -> bool:
        """Check if valid buvid3 is provided"""
        return buvid3 is not None and buvid3.strip() != ""
    

    
    def _check_credentials_with_api(self, sessdata: str, bili_jct: str, buvid3: str) -> bool:
        """
        Validate credentials via Bilibili API
        
        Args:
            sessdata: Bilibili session data
            bili_jct: Bilibili CSRF token
            buvid3: Bilibili user identifier
            
        Returns:
            bool: Whether credentials are valid
            
        Raises:
            ValueError: API response error or invalid credentials
            httpx.RequestError: Network request error
        """
        url = "https://api.bilibili.com/x/web-interface/nav"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.bilibili.com/"
        }
        
        cookies = {
            "SESSDATA": sessdata,
            "bili_jct": bili_jct,
            "buvid3": buvid3
        }
        
        try:
            response = httpx.get(url, headers=headers, cookies=cookies, timeout=15)
            response.raise_for_status()
            
            try:
                data = response.json()
            except ValueError as e:
                raise ValueError(f"API response format error, unable to parse JSON: {str(e)}")
            
            # Check API response
            code = data.get("code", -1)
            message = data.get("message", "")
            
            if code == 0:
                # Validation successful, check user information
                user_data = data.get("data", {})
                is_login = user_data.get("isLogin", False)
                if user_data and is_login:
                    return True
                else:
                    raise ValueError("User not logged in or login status invalid")
            elif code == -101:
                raise ValueError("Account not logged in, please check if SESSDATA is correct")
            elif code == -111:
                raise ValueError("CSRF validation failed, please check if bili_jct is correct")
            elif code == -400:
                raise ValueError("Request error, please check if all credentials are correct")
            elif code == -403:
                raise ValueError("Insufficient access permissions, credentials may have expired")
            elif code == -412:
                raise ValueError("Request was intercepted, please try again later")
            else:
                raise ValueError(f"API returned error: {message} (error code: {code})")
                
        except httpx.TimeoutException:
            raise httpx.RequestError("Request timeout")
        except httpx.ConnectError:
            raise httpx.RequestError("Connection error, unable to access Bilibili server")
        except httpx.HTTPStatusError as e:
            raise httpx.RequestError(f"HTTP error: {e}")
        except httpx.RequestError as e:
            raise httpx.RequestError(f"Network request failed: {e}")

    #########################################################################################
    # If OAuth is supported, uncomment the following functions.
    # Warning: please make sure that the sdk version is 0.4.2 or higher.
    #########################################################################################
    # def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    #     """
    #     Generate the authorization URL for bilibili_subtitle_plugin OAuth.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR AUTHORIZATION URL GENERATION HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return ""
        
    # def _oauth_get_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    # ) -> Mapping[str, Any]:
    #     """
    #     Exchange code for access_token.
    #     """
    #     try:
    #         """
    #         IMPLEMENT YOUR CREDENTIALS EXCHANGE HERE
    #         """
    #     except Exception as e:
    #         raise ToolProviderOAuthError(str(e))
    #     return dict()

    # def _oauth_refresh_credentials(
    #     self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    # ) -> OAuthCredentials:
    #     """
    #     Refresh the credentials
    #     """
    #     return OAuthCredentials(credentials=credentials, expires_at=-1)
