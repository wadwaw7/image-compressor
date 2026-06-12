"""邮箱校验工具 — 域名限制、格式校验"""

from __future__ import annotations

import re
from typing import Optional

from ..core.config import get_settings

settings = get_settings()

# 邮箱本地部分：仅允许字母数字和常见符号
_email_local_re = re.compile(r"^[A-Za-z0-9]+[A-Za-z0-9._\-]*$")

# 主流邮箱域名白名单
_MAINSTREAM_DOMAINS = {
    # QQ / 腾讯
    "@qq.com", "@foxmail.com", "@vip.qq.com",
    # 网易
    "@163.com", "@126.com", "@yeah.net",
    # Google
    "@gmail.com", "@googlemail.com",
    # Microsoft
    "@outlook.com", "@hotmail.com", "@live.com",
    # Yahoo
    "@yahoo.com", "@yahoo.co.jp",
    # 新浪 / 搜狐
    "@sina.com", "@sina.cn", "@sohu.com",
    # 阿里
    "@aliyun.com",
    # Apple
    "@icloud.com", "@me.com",
    # Proton
    "@proton.me", "@protonmail.com",
    # 其他常见
    "@zoho.com", "@mail.com", "@yandex.com",
}


def is_real_email(email: Optional[str]) -> bool:
    """是否为真实可投递邮箱（避免把 username@local 当成真实邮箱）。"""
    e = (email or "").strip().lower()
    return bool(e) and ("@" in e) and (not e.endswith("@local"))


def _allowed_domains() -> set[str]:
    """获取允许的邮箱域名（配置 + 主流域名默认值）。"""
    raw = getattr(settings, "ALLOWED_EMAIL_DOMAINS", "")
    if raw and raw.strip():
        domains = {d.strip().lower() for d in raw.split(",") if d.strip()}
        return domains
    # 默认：主流邮箱域名 + @local（占位）
    return _MAINSTREAM_DOMAINS | {"@local"}


def _validate_email_local(email: str) -> bool:
    """验证邮箱本地部分不包含危险字符"""
    if "@" not in email:
        return True
    local = email.split("@")[0]
    if not local:
        return False
    if not _email_local_re.match(local):
        return False
    return True


def get_email_domain(email: Optional[str]) -> str:
    """提取邮箱域名（小写），如 @qq.com"""
    e = (email or "").strip().lower()
    idx = e.find("@")
    return e[idx:] if idx >= 0 else ""


def is_allowed_register_email(email: Optional[str]) -> bool:
    """注册时允许的邮箱域名。允许为空。且验证本地部分无 XSS。"""
    e = (email or "").strip().lower()
    if not e:
        return True
    if not _validate_email_local(e):
        return False
    domains = _allowed_domains()
    return any(e.endswith(d) for d in domains)


def is_allowed_bind_email(email: Optional[str]) -> bool:
    """绑定/修改邮箱允许的域名。要求必须提供邮箱。且验证本地部分无 XSS。"""
    e = (email or "").strip().lower()
    if not e:
        return False
    if not _validate_email_local(e):
        return False
    domains = _allowed_domains()
    return any(e.endswith(d) for d in domains)


def get_allowed_domains_display() -> str:
    """返回允许的邮箱域名列表（用于错误提示）。"""
    domains = _allowed_domains() - {"@local"}
    sorted_domains = sorted(domains)
    return "、".join(sorted_domains[:10]) + ("等" if len(sorted_domains) > 10 else "")

