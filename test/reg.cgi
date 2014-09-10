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



my $sql=SQL::Abstract->new;
my ($stmt,@bind)=$sql->insert('users',
	{
		login=>$log,
		pass=>$pas,
		cookie=>$crypted_password
	}
);    
my $sth=$dbh->prepare($stmt);
$sth->execute(@bind);
my $q = CGI->new;
print  $q->redirect('http://localhost/test_html/aut.html');
print header(-type => "text/html", -charset=>'utf8');
$dbh->disconnect();









