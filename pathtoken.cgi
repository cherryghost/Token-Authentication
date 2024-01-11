#!/bin/bash
# Path token UI v1.4 - Alan Brierton 2019 - It's a bit shoddy. I've lost my 1.5 and 1.6 version. No interest to fix the problems anymore
echo "Content-type: text/html"
echo ""

echo '<html>'
echo '<head>'
echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
echo '<title>Path Token UI</title>'
echo '</head>'
echo '<body>'

  echo '<p style="font-size:120%;">Path Token UI v1.4</p>'\
       "<form method=GET action=\"${SCRIPT}\">"\
       '<table border="1"><col width="150"><col width="400"'\
          '<tr><td>Secret</TD><TD><input type="text" name="val_a" size=62></td></tr>'\
          '<tr><td>Path</td><td><input type="text" name="val_b" size=62 value=""></td></tr>'\
          '<tr><td>Filename</td><td><input type="text" name="val_c" size=62 value=""></td></tr>'\
          '<tr><td>Number of Directories</TD><TD><input type="text" name="val_d" size=62></td></tr>'\
          '<tr><td>IP</TD><TD><input type="text" name="val_y" size=62></td></tr>'\
          '<tr><td>Name of not-valid-after</TD><TD><input type="text" name="val_f" size=62></td></tr>'\
          '<tr><td>nva</TD><TD><input type="text" name="val_g" size=62></td></tr>'\
          '<tr><td>Generation</TD><TD><input type="text" name="val_h" size=62></td></tr>'\
          '<tr><td>Name of Hash</TD><TD><input type="text" name="val_z" size=62></td></tr>'\
          '</table>'

  echo '<br><input type="submit" value="Process Form"></form>'\
       '<form action="pathtoken.cgi"><input type="submit" value="Reset" /></form>'

  # Make sure we have been invoked properly.

  if [ "$REQUEST_METHOD" != "GET" ]; then
        echo "<hr>Script Error:"\
             "<br>Usage error, cannot complete request, REQUEST_METHOD!=GET."\
             "<br>Check your FORM declaration and be sure to use METHOD=\"GET\".<hr>"
        exit 1
  fi

  # If no search arguments, exit gracefully now.

  if [ -z "$QUERY_STRING" ]; then
        exit 0
  else
     # No looping this time, just extract the data you are looking for with sed:
     secret=`echo "$QUERY_STRING" | sed -n 's/^.*val_a=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%3D/=/g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     path=`echo "$QUERY_STRING" | sed -n 's/^.*val_b=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%3D/=/g" |sed "s/%26/&/g" | sed "s/%2F/\//g"`
     file=`echo "$QUERY_STRING" | sed -n 's/^.*val_c=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%3D/=/g" |sed "s/%26/&/g" | sed "s/%2F/\//g"`
     dirs=`echo "$QUERY_STRING" | sed -n 's/^.*val_d=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%3D/=/g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     ip=`echo "$QUERY_STRING" | sed -n 's/^.*val_y=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%3D/=/g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     nva_pref=`echo "$QUERY_STRING" | sed -n 's/^.*val_f=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     nva=`echo "$QUERY_STRING" | sed -n 's/^.*val_g=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     gen=`echo "$QUERY_STRING" | sed -n 's/^.*val_h=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     hashkey=`echo "$QUERY_STRING" | sed -n 's/^.*val_z=\([^&]*\).*$/\1/p' | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     question=`echo "?" | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     ipresult=`echo "&ip=" | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`
     dirsamp=`echo "&dirs=" | sed "s/%20/ /g" | sed "s/%26/&/g" | sed "s/%2F/\//g"`

   if [ -z "$ip" ]; then
       token=`echo -n $path?$nva_pref=$nva$dirsamp$dirs | openssl sha1 -hmac $secret -binary | xxd -p | cut -c1-20`
       echo "Full Authorized Path:           /token=$nva_pref=$nva~dirs=$dirs~$hashkey=$gen$token$path$file"
   else
       token=`echo -n $path?$nva_pref=$nva$ipresult$ip$dirsamp$dirs | openssl sha1 -hmac $secret -binary | xxd -p | cut -c1-20`
       echo "Full Authorized Path:           /token=$nva_pref=$nva~ip=$ip~dirs=$dirs~hash=$gen$token$path$file"
   fi
  fi
echo '</body>'
echo '</html>'

exit 0
