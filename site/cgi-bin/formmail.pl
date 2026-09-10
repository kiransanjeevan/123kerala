<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Error: GET request</title>
    <style type="text/css">
    <!--
       body {
              background-color: #FFFFFF;
              color: #000000;
             }
       p.c2 {
              font-size: 80%;
              text-align: center;
            }
       th.c1 {
               text-align: center;
               font-size: 143%;
             }
       p.c3 {font-size: 80%; text-align: center}
       div.c2 {margin-left: 2em}
     -->
    </style>
  </head>
  <body>
    <table border="0" width="600" bgcolor="#9C9C9C" summary="">
      <tr bgcolor="#9C9C9C">
        <th class="c1">Error: GET request</th>
      </tr>
      <tr bgcolor="#CFCFCF">
        <td>
          <p>
  The HTML form fails to specify the POST method, so it would not
  be correct for this script to take any action in response to
  your request.
</p>
<p>
  If you are attempting to configure this form to run with FormMail,
  you need to set the request method to POST in the opening form tag,
  like this:
  <tt>&lt;form action=&quot;/cgi-bin/FormMail.pl&quot; method=&quot;post&quot;&gt;</tt>
</p>

          <hr size="1" />
          <p class="c3">
            <a href="http://nms-cgi.sourceforge.net/">FormMail</a>
            &copy; 2001-2003 London Perl Mongers
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>
