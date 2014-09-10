#!/usr/bin/perl
use 5.010;
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use DBI; 
use SQL::Abstract;
use Template;
use Data::Dumper;
use utf8;
use CGI::Cookie; 

my $dbh = DBI->connect('DBI:mysql:test_1:localhost','root','123456')
    or  die "Error! Can not connect:". $DBI::errstr;
$dbh->do("SET NAMES utf8");

my $log= param("login");
my $pas=param("password");
my @saltair = ('A', 'f');
my $salt = $saltair[0] . $saltair[1];;
my $crypted_password = crypt($pas, $salt);
=f
my $cookie=new CGI::Cookie(
      -name => 'pas',
      -value => $crypted_password,
      -expires => '+1d',
      -path => '/cgi-bin/test/',
      -domain => '.localhost'     
        );
=cut        

  sub authentication {
  	my $sql = SQL::Abstract->new;
    my ($stmt,@bind) = $sql->select('users', [qw/id_user/],[{login=>$log,pass=>$pas,cookie=>$crypted_password}]);
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    my $id=$sth -> fetchrow_array;
    defined $id?return 1: return 0; 
  }

my $q = CGI->new;
my $cookie = $q->cookie(
  -name => 'pas',
  -value => $crypted_password,
  -expires => '+1d',
  -path => '/cgi-bin/test/',
  -domain => '.localhost'   
  );
print $q->header(
     -type    => 'text/html',
     -expires => '+1d',
     -charset=>'utf8',
     -cookie  => $cookie
     );

if (my $authentication=authentication()== 0) {
  	
    #print  $q->redirect('http://localhost/test_html/reg.html');
     #print q~ <a href="http://localhost/test_html/reg.html">зарегестрируйся</a>~;
     print qq~<html><head><title>Подождите...</title>~;
     print qq~<meta http-equiv="refresh" content="2;url=http://localhost/test_html/reg.html">~;
}  else {
	
  #print  $q->redirect('http://localhost/cgi-bin/test/template.cgi');
  # print q~ <a href="http://localhost/cgi-bin/test/template.cgi">пройди тест</a>~;
  print qq~<html><head><title>Подождите...</title>~;
  print qq~<meta http-equiv="refresh" content="2;url=http://localhost/cgi-bin/test/template.cgi">~;
}   

#print header(-type => "text/html", -charset=>'utf8', -cookie=>$cookie );


$dbh->disconnect();

	
 	
