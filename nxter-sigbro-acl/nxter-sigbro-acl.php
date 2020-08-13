<?php
/*
Plugin Name: NXTER SIGBRO ACL
Plugin URI: https://www.nxter.org/sigbro
Version: 0.1.0
Author: scor2k
Description: Check account property for the users
License: GPLv2 or later.
License URI: http://www.gnu.org/licenses/gpl-2.0.html
 */?>
<?php

defined('ABSPATH') or die('No script kiddies please!');

function sigbro__post_json($url, $params, $timeout = 3)
{
    $res = @file_get_contents($url, false, stream_context_create(array(
        'http' => array(
            'method' => 'POST',
            'header' => 'Content-type: application/x-www-form-urlencoded',
            'content' => http_build_query($params),
            'timeout' => $timeout,
        ),
    )));
    return $res;
}

function sigbro__get_json($url, $timeout = 3) {
    $res = @file_get_contents($url, false, stream_context_create(array(
        'http' => array(
            'method' => 'GET',
            'header' => 'Content-type: application/x-www-form-urlencoded',
            'timeout' => $timeout,
        ),
    )));
    return $res;
}

function sigbro__is_user_member($user) {
  $url = "https://random.api.nxter.org/tstardor?requestType=getAccountProperties&recipient=" . $user . "&property=sigbro&setter=ARDOR-H2W5-VZAB-9XFZ-38885";
  $res = sigbro__get_json($url);

  if (!$res) { 
    return 'guest';
  } else {
    $res = json_decode($res, true);
  }

  if ( isset($res['properties']) && count($res['properties']) > 0 ) {
    $status = $res['properties'][0]['value'];
    return $status;
  }

  return 'guest';
} 

add_filter('the_content', 'sigbro__check_acl');

function sigbro__check_acl($content) {
  $pattern = "/\[sigbro_acl\]/";
  preg_match_all($pattern, $content, $result); //find all 
  $current_user = wp_get_current_user();
  $account = $current_user->user_login;
  if ( $account == False ) { 
    // anon user
    $content = '<h2>Access Deny</h2><p>You should be a Sigbro Member</p>';

  } else if ( count($result[0]) > 0 ) { 
    // check user's status
    $status = sigbro__is_user_member($account);
    if ( $status == 'guest' ) {
      $content = '<h2>Access Deny</h2><p>You should be a Sigbro Member</p>';
    } else {
      $content = str_replace('[sigbro_acl]', '', $content);
    } 


  }
  return $content;
}



?>

