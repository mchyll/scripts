# Definer parametre for FTP-server, paths, credentials osv
$scriptSourceFtp = @{
    url = "ftp://test.no/sql";
    username = "test";
    password = "123"
}

$tempDirectory = "temp"

$dataDestinationFtp = @{
    url = "";
    username = "";
    password = ""
}

# Laste ned SQL-spørring fra en FTP-server og lagre den i en fil lokalt
$downloadFtp = New-Object System.Net.WebClient
$downloadFtp.Credentials = New-Object System.Net.NetworkCredential($scriptSourceFtp.username, $scriptSourceFtp.password)


# Kjøre SQL-spørring fra lokal fil vha. sqlcmd, lagre data til lokal midlertidig mappe


# For hver fil i midlertidig mappe:
    # Last opp til tredjeparts FTP-server
    # Slett fila lokalt