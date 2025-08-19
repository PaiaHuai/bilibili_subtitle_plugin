from typing import Any
import httpx
import urllib.parse
import logging
from dify_plugin.config.logger_format import plugin_logger_handler
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)


class BilibiliSubtitlePluginProvider(ToolProvider):
    
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证B站凭证的有效性
        
        Args:
            credentials: 包含凭证信息的字典
            
        Raises:
            ToolProviderCredentialValidationError: 当凭证验证失败时
        """
        logger.info("Starting Bilibili credential validation")
        
        # 1. 提取凭证信息
        sessdata = credentials.get("sessdata", "")
        bili_jct = credentials.get("bili_jct", "")
        buvid3 = credentials.get("buvid3", "")
        
        # 2. 验证凭证完整性
        logger.info("Step 1: Validating credential completeness")
        self._validate_credentials_completeness(sessdata, bili_jct, buvid3)
        logger.info("✓ Credential completeness validation passed")
        
        # 3. 通过API验证凭证有效性
        logger.info("Step 2: Validating credentials via API")
        self._validate_credentials_with_api(sessdata, bili_jct, buvid3)
        logger.info("✓ API credential validation passed")
        
        logger.info("Bilibili credential validation completed, all checks passed")
    
    def _validate_credentials_completeness(self, sessdata: str, bili_jct: str, buvid3: str) -> None:
        """验证凭证完整性"""
        if not self._has_sessdata(sessdata):
            logger.error("SESSDATA validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("缺少必要的凭证信息：SESSDATA。请确保已正确配置所有必需的凭证字段。")
        
        if not self._has_bili_jct(bili_jct):
            logger.error("bili_jct validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("缺少必要的凭证信息：bili_jct。请确保已正确配置所有必需的凭证字段。")
        
        if not self._has_buvid3(buvid3):
            logger.error("buvid3 validation failed: credential is empty or too short")
            raise ToolProviderCredentialValidationError("缺少必要的凭证信息：buvid3。请确保已正确配置所有必需的凭证字段。")
    

    
    def _validate_credentials_with_api(self, sessdata: str, bili_jct: str, buvid3: str) -> None:
        """
        通过API验证凭证有效性
        
        Args:
            sessdata: 用户会话数据
            bili_jct: CSRF令牌  
            buvid3: 浏览器唯一标识
            
        Raises:
            ToolProviderCredentialValidationError: 凭证验证失败
        """
        try:
            # 调用API验证凭证
            is_valid = self._check_credentials_with_api(sessdata, bili_jct, buvid3)
            if not is_valid:
                raise ToolProviderCredentialValidationError("凭证验证失败：凭证无效或已过期。请检查凭证是否正确或尝试重新获取。")
                
        except ValueError as e:
            # API响应相关的错误（如登录状态、错误码等）
            raise ToolProviderCredentialValidationError(f"凭证验证失败：{str(e)}")
            
        except httpx.RequestError as e:
            # 网络相关的错误
            error_msg = str(e)
            if "超时" in error_msg or "timeout" in error_msg.lower():
                raise ToolProviderCredentialValidationError("凭证验证失败：网络请求超时，请检查网络连接后重试")
            elif "连接" in error_msg or "connection" in error_msg.lower():
                raise ToolProviderCredentialValidationError("凭证验证失败：无法连接到B站服务器，请检查网络设置")
            else:
                raise ToolProviderCredentialValidationError(f"凭证验证失败：网络请求异常 - {error_msg}")
                
        except Exception as e:
            # 其他未预期的错误
            raise ToolProviderCredentialValidationError(f"凭证验证失败：发生未知错误 - {str(e)}")
    
    def _has_sessdata(self, sessdata: str) -> bool:
        """检查是否提供有效的SESSDATA"""
        return sessdata is not None and sessdata.strip() != ""
    
    def _has_bili_jct(self, bili_jct: str) -> bool:
        """检查是否提供有效的bili_jct"""
        return bili_jct is not None and bili_jct.strip() != ""
    
    def _has_buvid3(self, buvid3: str) -> bool:
        """检查是否提供有效的buvid3"""
        return buvid3 is not None and buvid3.strip() != ""
    

    
    def _check_credentials_with_api(self, sessdata: str, bili_jct: str, buvid3: str) -> bool:
        """
        通过B站API验证凭证有效性
        
        Args:
            sessdata: B站会话数据
            bili_jct: B站CSRF令牌
            buvid3: B站用户标识
            
        Returns:
            bool: 凭证是否有效
            
        Raises:
            ValueError: API响应错误或凭证无效
            httpx.RequestError: 网络请求错误
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
                raise ValueError(f"API响应格式错误，无法解析JSON: {str(e)}")
            
            # 检查API响应
            code = data.get("code", -1)
            message = data.get("message", "")
            
            if code == 0:
                # 验证成功，检查用户信息
                user_data = data.get("data", {})
                is_login = user_data.get("isLogin", False)
                if user_data and is_login:
                    return True
                else:
                    raise ValueError("用户未登录或登录状态无效")
            elif code == -101:
                raise ValueError("账号未登录，请检查SESSDATA是否正确")
            elif code == -111:
                raise ValueError("CSRF校验失败，请检查bili_jct是否正确")
            elif code == -400:
                raise ValueError("请求错误，请检查所有凭证是否正确")
            elif code == -403:
                raise ValueError("访问权限不足，凭证可能已过期")
            elif code == -412:
                raise ValueError("请求被拦截，请稍后重试")
            else:
                raise ValueError(f"API返回错误：{message} (错误码: {code})")
                
        except httpx.TimeoutException:
            raise httpx.RequestError("请求超时")
        except httpx.ConnectError:
            raise httpx.RequestError("连接错误，无法访问B站服务器")
        except httpx.HTTPStatusError as e:
            raise httpx.RequestError(f"HTTP错误: {e}")
        except httpx.RequestError as e:
            raise httpx.RequestError(f"网络请求失败: {e}")

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
