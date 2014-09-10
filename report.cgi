#!/usr/bin/perl
use v5.14.2;
use strict;
use warnings;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);
use DBI; 
use SQL::Abstract;
use Template;
use Data::Dumper;
use utf8;
use Encode;
use lib qw( /usr/local/lib/perl5/site_perl/5.20.0/x86_64-linux     );
#use Class::Date qw(:errors date localdate gmdate now -DateParse -EnvC);

 #это спасает от кракозябры в брауезе!

print header(-type => "text/html", -charset=>'utf8');
my $dbh = DBI->connect('DBI:mysql:test_1:localhost','root','123456')
    or  die "Error! Can not connect:". $DBI::errstr;
$dbh->do("SET NAMES utf8");
$dbh->do("SET CHARACTER SET utf8");

$Data::Dumper::Indent =1;
$Data::Dumper::Useqq = 1;

{ no warnings 'redefine';
    sub Data::Dumper::qquote {
        my $s = shift;
        return "'$s'";
    }
}

my $cookie= cookie("pas");
my $now = now;
my $date=$now->string ; 
no lib qw( /usr/local/lib/perl5/site_perl/5.20.0/x86_64-linux );

sub get_id_user {
	my $sql = SQL::Abstract->new;
    my ($stmt,@bind) = $sql->select('users', [qw/id_user/],[{cookie=>$cookie }]);
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    my $id=$sth -> fetchrow_array;
    return  $id;
}   

my $id= get_id_user;

sub get_user_answers {
	my $query = CGI->new;
    my @names = $query->param;
    my @arr=map{param($_);}@names;
    my $last=pop (@arr);
	return @arr;
}
my @answer=get_user_answers;

sub get_true_answer {
	my $sql = SQL::Abstract->new;
    my ($stmt,@bind) = $sql->select('answers', [qw/answer/],[{flag=>1}]);
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    my @answer;
 	while (my $answer=$sth -> fetchrow_array) {
 		push @answer, $answer;
 	}
 	return @answer;
}
my @true_answer= get_true_answer(); 

sub convert_str {
	my $str= shift;
	$str=~s/\s//g;
	my @count=  split '', $str;
    my $count= @count;  
}

my @res = map {
    my $i=$_;  
 	    if ($answer[$i] eq $true_answer[$i]) {
    	$answer[$i];
    } elsif ($i ==1 ) {
    	my $count_1=convert_str($answer[$i]);
    	my $count_2=convert_str($true_answer[$i]);
    	if ($count_1 == $count_2) {
    		$answer[$i];
    	}
    } 
} 0..@true_answer; 

sub get_id_answer {
	my $sql = SQL::Abstract->new;
    my ($stmt,@bind) = $sql->select('answers', [qw/id_answer/],[{flag=>1}]);
    my $sth = $dbh->prepare($stmt);
    $sth->execute(@bind);
    my @id_answer;
 	while (my $id_answer=$sth -> fetchrow_array) {
 		push @id_answer, $id_answer;
 	}
 	return @id_answer;
}	

my @id_answer= get_id_answer;

@id_answer=map{
	my $ind=$_;
	my $sql=SQL::Abstract->new;
	my ($stmt,@bind)=$sql->insert('user_answers',
		{
			id_user=> $id, 
			quest=>$ind+1,
		    answer=>$id_answer[$ind],
		    user_answer=>$answer[$ind],
		    date=>$date

	    }
	);  
    my $sth=$dbh->prepare($stmt);
    $sth->execute(@bind) or die $sth->errstr;
}0..@id_answer-1;

@res= grep {$_ ne  undef}@res;
my $count_answer=@res; 
my $count_quest=@answer;

my $tt2 = Template->new({
	INCLUDE_PATH => '/var/www/test_html',
    DEFAULT_ENCODING => 'utf8',
    ENCODING => 'utf8',
}) || die "$tt2::ERROR\n";

my $var={
	amount_answer=>$count_answer,
	amount_quest=>$count_quest
};
$tt2->process('report.html', $var) || die $tt2->error(), "\n";
$dbh->disconnect();


