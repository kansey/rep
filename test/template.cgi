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
use encoding 'utf8'; 
print header(-type => "text/html", -charset=>'utf8');

my $dbh = DBI->connect('DBI:mysql:test_1:localhost','root','123456')
              or  die "Error! Can not connect:". $DBI::errstr;
$dbh->do("SET NAMES utf8");

sub get_id_quest {
    my $sql = SQL::Abstract->new;
    my $stmt= $sql->select('questions',[qw/id_quest quest/]);
    my $ary_ref  = $dbh->selectall_arrayref($stmt, { Slice => {} });
    return $ary_ref;
    }
# возвращаем ссылку на массивхешей
my $ref_questions= get_id_quest;

sub get_answers {
    my $id_quest=shift;
    my $sql = SQL::Abstract->new;
    my ($stmt,@bind) = $sql->select('answers', [qw/id_quest,answer/],[{id_quest=>$id_quest}]);
    my $ary_ref  = $dbh->selectall_arrayref($stmt,{ Slice => {} },@bind);
    return $ary_ref;
    }
$_->{answers} = get_answers($_->{id_quest}) for @$ref_questions;
my $tt2 = Template->new({
    INCLUDE_PATH => '/var/www/test_html',
    DEFAULT_ENCODING => 'utf8',
    ENCODING => 'utf8',}
    )|| die "$tt2::ERROR\n";

my $var={id_quest_answer =>$ref_questions};
$tt2->process('temp.html', $var) || die $tt2->error(), "\n";
$dbh->disconnect();
