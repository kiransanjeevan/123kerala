<!--
#####################################################################
#                                                                   #
#    Copyright © 1999-2001 CGISCRIPT.NET - All Rights Reserved     #
#                                                                   #
#####################################################################
#                                                                   #
#          THIS COPYRIGHT INFORMATION MUST REMAIN INTACT            #
#                AND MAY NOT BE MODIFIED IN ANY WAY                 #
#                                                                   #
#####################################################################
#
# When you downloaded this script you agreed to accept the terms
# of this Agreement. This Agreement is a legal contract, which
# specifies the terms of the license and warranty limitation between
# you and CGISCRIPT.NET. You should carefully read the following
# terms and conditions before installing or using this software.
# Unless you have a different license agreement obtained from
# CGISCRIPT.NET, installation or use of this software indicates
# your acceptance of the license and warranty limitation terms
# contained in this Agreement. If you do not agree to the terms of this
# Agreement, promptly delete and destroy all copies of the Software.
#
# Versions of the Software
# Only one copy of the registered version of CGISCRIPT.NET
# may used on one web site.
#
# License to Redistribute
# Distributing the software and/or documentation with other products
# (commercial or otherwise) or by other than electronic means without
# CGISCRIPT.NET's prior written permission is forbidden.
# All rights to the CGISCRIPT.NET software and documentation not expressly
# granted under this Agreement are reserved to CGISCRIPT.NET.
#
# Disclaimer of Warranty
# THIS SOFTWARE AND ACCOMPANYING DOCUMENTATION ARE PROVIDED "AS IS" AND
# WITHOUT WARRANTIES AS TO PERFORMANCE OF MERCHANTABILITY OR ANY OTHER
# WARRANTIES WHETHER EXPRESSED OR IMPLIED.   BECAUSE OF THE VARIOUS HARDWARE
# AND SOFTWARE ENVIRONMENTS INTO WHICH CGISCRIPT.NET MAY BE USED, NO WARRANTY
# OF FITNESS FOR A PARTICULAR PURPOSE IS OFFERED.  THE USER MUST ASSUME THE
# ENTIRE RISK OF USING THIS PROGRAM.  ANY LIABILITY OF CGISCRIPT.NET WILL BE
# LIMITED EXCLUSIVELY TO PRODUCT REPLACEMENT OR REFUND OF PURCHASE PRICE.
# IN NO CASE SHALL CGISCRIPT.NET BE LIABLE FOR ANY INCIDENTAL, SPECIAL OR
# CONSEQUENTIAL DAMAGES OR LOSS, INCLUDING, WITHOUT LIMITATION, LOST PROFITS
# OR THE INABILITY TO USE EQUIPMENT OR ACCESS DATA, WHETHER SUCH DAMAGES ARE
# BASED UPON A BREACH OF EXPRESS OR IMPLIED WARRANTIES, BREACH OF CONTRACT,
# NEGLIGENCE, STRICT TORT, OR ANY OTHER LEGAL THEORY. THIS IS TRUE EVEN IF
# CGISCRIPT.NET IS ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. IN NO CASE WILL
# CGISCRIPT.NET' LIABILITY EXCEED THE AMOUNT OF THE LICENSE FEE ACTUALLY PAID
# BY LICENSEE TO CGISCRIPT.NET.
#####################################################################
#                                                                   #
# Credits:                                                          #
# Andy Angrick - Programmer - angrick@cgiscript.net                 #
# Mike Barone  - Developer  - mbarone@cgiscript.net                 #
#                                                                   #
# For information about this script or other scripts please see :   #
# http://www.cgiscript.net                                          #
#                                                                   #
# Thank you for trying out our script.                              #
# If you have any suggestions or ideas for a new innovative script  #
# please direct them to suggest@cgiscript.net.   Thanks.            #
#                                                                   #
#####################################################################
--><html>

<head>
<title>csBanner</title>
<style>
<!--
 INPUT.button { background-color:#eeeeee;font:verdana;font-weight:bold;color:#000080;font-size:10pt; }
-->
</style>
</head>

<body>

<form method="POST" action="http://www.123kerala.com/cgi-script/csBanner/csBanner.cgi" name="form1" onSubmit="return SetPass();">
  <input type="hidden" name="command" value="manage">
  <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
    <tr>
      <td>
      <div align="center">
        <center>
        <table border="0" cellpadding="5" cellspacing="0" bgcolor="#135184" style="border-collapse: collapse" bordercolor="#111111">
          <tr>
            <td>
            <div align="center">
              <table border="1" cellpadding="3" cellspacing="0" bordercolorlight="#000000" bordercolordark="#FFFFFF">
                <tr>
                  <td>
                  <div align="center">
                    <table border="0" cellpadding="3" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111">
                      <tr>
                        <td colspan="2" align="center">
                        <p align="center">
                        <img border="0" src="http://www.123kerala.com/cgi-script/csBanner/banners/logo_login.gif" width="250" height="75"></p>
                        </td>
                      </tr>
                      <tr>
                        <td align="right">
                        <font size="2" face="verdana,arial,helvetica" color="#D6D6D6">
                        <b>Username:</b></font></td>
                        <td>
                        <font face="verdana,arial,helvetica" size="2" color="#FFFFFF">
                        <b><input type="text" name="UserName" size="20"></b></font></td>
                      </tr>
                      <tr>
                        <td align="right">
                        <font size="2" face="verdana,arial,helvetica" color="#D6D6D6">
                        <b>Password:</b> </font></td>
                        <td>
                        <font face="verdana,arial,helvetica" size="2" color="#FFFFFF">
                        <b><input type="password" name="PassWord" size="20"></b></font></td>
                      </tr>
                      <tr>
                        <td colspan="2" align="center">
                        <hr noshade size="1" color="#000000">
                        </td>
                      </tr>
                      <tr><td align="center" colspan="2" valign="middle"><input CLASS="button" type="submit" value="     Login     " name="B1"><img border="0" src="http://www.cgiscript.net/spacer.gif" width="1" height="1"></td></tr></table></div></td></tr>
                </center>
              </table>
            </div>
            </td>
          </tr>
        </table>
      </div>
      </td>
    </tr>
  </table>
</form>

</body>
<script language="javascript">
document.form1.UserName.focus();
function SetPass(){
var UserName = document.form1.UserName.value;
var PassWord = document.form1.PassWord.value;
if(!UserName){
alert("Error. Please enter a username");
return false;
}
if(!PassWord){
alert("Error. Please enter a password");
return false;
}
document.cookie = "UserName="+UserName;
document.cookie = "PassWord="+PassWord;
return true;
}
        </script>

</html>