#!"C:\Strawberry\perl\bin\perl.exe"

use warnings; 
use strict;
use CGI qw(:standard);
use DBI;
use HTML::Parser;
use JSON;
binmode STDOUT, ":utf8";
use utf8;

#connect to the DB
my $driver = "SQLite";
my $database = "database.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, {RaiseError=> 1}) or die $DBI::errstr;

my $cgi = new CGI;
print $cgi->header('text/html');

my $dateset = param('date') if (param('date'));
my $timeset = param('time') if (param('time'));
my $descset = param('description') if (param('description'));

# if there is params it's a POST, create new record
if ($dateset && $timeset && $descset) {
	print $cgi->start_html(-title=>'Appointed Output');
	print "Date: $dateset | Time: $timeset | Description: $descset will be added to the database";

	my $stmt = q/INSERT INTO appointments (date, time, desc) VALUES (?,?,?)/;
	my $sth = $dbh->prepare($stmt);
	$sth->execute($dateset, $timeset, $descset);
	print "Done!";
	#Reroute to the same page
	print '<meta http-equiv="refresh" content="1;url=http://localhost/app/">';
} else # else it's a get request, list the data
{
	my @output;

	my $sth = $dbh->prepare('select * from appointments'); #our table is named appointed.
	$sth -> execute;

	while(my $row = $sth->fetchrow_hashref) {
		push @output, $row;
	}
	print to_json({data=> \@output});
}
$dbh->disconnect();
