from pytest_mysql import factories


mysql_noproc = factories.mysql_noproc()
mysql = factories.mysql("mysql_noproc")
