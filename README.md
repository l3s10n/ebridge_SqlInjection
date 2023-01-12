# 概述

由于WxMpFollowerInviteController中sql语句的执行方式不当，在登录泛微云桥之后，可以进行sql注入。

# 影响版本

versions <= 最新(20221013)

# 原理

这里是WxMpFollowerInviteController的loadFollowerInvites的关键代码：

```java
public void loadFollowerInvites() {
    try {
        String fromuser = this.getPara("fromuser");
        String touser = this.getPara("touser");
        String starttime = this.getPara("starttime");
        String endtime = this.getPara("endtime");
        this.renderJson(this.wxMpFollowerInviteService.loadFollowerInvites(fromuser, touser, starttime, endtime));
    } catch (Exception var5) {
        this.log.error(var5.getMessage(), var5);
        this.renderJsonMsg("程序异常，请联系管理员！", false);
    }

}
```

可以看到，`fromuser`、`touser`、`starttime`、`endtime`都是可控的，他们会传入到`this.wxMpFollowerInviteService.loadFollowerInvites`方法中，并最终调用WxMpFollowerInviteModel的loadFollowerInvites方法，该方法的关键代码如下：

```java
public List<WxMpFollowerInviteModel> loadFollowerInvites(String fromuser, String touser, String starttime, String endtime) {
    StringBuffer sql = new StringBuffer();
    sql.append("select a.createdate, b.nickname, d.name from wx_mp_follower_invite a left join wx_mp_follower b on a.openid = b.openid and a.sysappid = b.sysappid");
    sql.append(" left join wx_cp_user_account c on a.outsysid = c.outsysid and a.outsysuserid = c.outsysuserid");
    sql.append(" left join wx_cp_userinfo d on c.userid = d.id where d.syscorpid = ?");
    if (!StrKit.isBlank(fromuser)) {
        sql.append(" and d.name like '%");
        sql.append(fromuser);
        sql.append("%'");
    }

    if (!StrKit.isBlank(touser)) {
        sql.append(" and b.nickname like '%");
        sql.append(touser);
        sql.append("%'");
    }

    if (!StrKit.isBlank(starttime)) {
        sql.append(" and unix_timestamp(a.createdate) >= unix_timestamp('");
        sql.append(starttime);
        sql.append("')");
    }

    if (!StrKit.isBlank(endtime)) {
        sql.append(" and unix_timestamp(a.createdate) <= unix_timestamp('");
        sql.append(endtime);
        sql.append("')");
    }

    return this.find(sql.toString(), new Object[]{ToolProp.getPropValue("basedoc", "syscorpid")});
}
```

可以看到，我们输入的`fromuser`、`touser`、`starttime`、`endtime`都会被拼接到sql语句中执行，我们只需要设置`fromuser`为`%' union select ({sql}), 123, 123 from information_schema.tables where table_schema!='`即可执行sql语句。

# 演示

见本仓库的Demonstrate.mp4文件。

# EXP

见本仓库的exp.py，使用方式是配置exp.py中目标的信息以及要执行的sql语句，执行exp.py，exp.py会打印sql语句执行的结果。

演示中使用的exp就是这里的exp

# 免责声明

本仓库仅用于学习使用，请勿用于实际场景，一切后果由使用者自负。
