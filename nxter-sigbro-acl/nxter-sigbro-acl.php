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

function access_deny_page() {
  //$content = '<center><h2>Access Deny</h2></center>';
  //$content .= '<center>You are NOT a member of our club for Cool Kids</center>';
  //$content .= '<center>(e.g., there is no valid ticket/membership token in your account)</center>';
  //$content .= '<br>';
  //$content .= 'The good news is that you can join us. <a href="https://demo.sigbro.app/copy/">Click here to become a member</a>';
  $content = '[fl_builder_insert_layout id="267"]';

  return $content;
}

function access_deny_vip_page() {
  //$content = '<center><h2>Access Deny</h2></center>';
  //$content .= '<center>You are NOT a member of our club for Cool Kids</center>';
  //$content .= '<center>(e.g., there is no valid ticket/membership token in your account)</center>';
  //$content .= '<br>';
  //$content .= 'The good news is that you can join us. <a href="https://demo.sigbro.app/copy/">Click here to become a member</a>';
  $content = '[fl_builder_insert_layout id="322"]';

  return $content;
}



function sigbro__check_acl($content) {

  if ( !is_page() ) {
    return $content;
  }

  $pattern = "/\[sigbro_acl\]/";
  $pattern_gold = "/\[sigbro_acl_vip\]/";

  preg_match_all($pattern, $content, $result); //find all 
  preg_match_all($pattern_gold, $content, $result_vip); //find all 

  $current_user = wp_get_current_user();
  $account = $current_user->user_login;
  if ( count($result[0]) > 0 ) { 
    // check user's status

    if ( $account == False ) {
      $content = access_deny_page();
    } else {
      $status = sigbro__is_user_member($account);
      //print("member:".$status);
      if ( $status == 'guest' ) {
        $content = access_deny_page();
      } else {
        $content = str_replace('[sigbro_acl]', '', $content);
      }
    }
  } elseif (count($result_vip[0]) > 0) {
    // check if user silver+ member
    if ( $account == False ) {
      $content = access_deny_page();
    } else {
      $status = sigbro__is_user_member($account);
      //print("vip:".$status);
      if ( $status == 'guest' ) {
        $content = access_deny_page();
      } elseif ( $status == 'member' ) {
        $content = access_deny_vip_page();
      } else {  
        $content = str_replace('[sigbro_acl_vip]', '', $content);
      }
    }

  } 


  return $content;
}



?>

