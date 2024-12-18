
		
rm web -r -force
md web
md web\logs
copy-item src web\src -force -recurse 
copy-item APIs web\APIs -force -recurse 
copy-item api_service.py web -force -recurse
copy-item .env web -force -recurse 
copy-item app_config.py web -force -recurse 
copy-item web.config web -force -recurse
copy-item resources web\resources -force -recurse

cd web

$config = (Get-Content -Raw ".env" | ConvertFrom-StringData)


(Get-Content -Path .env) |
    ForEach-Object {$_ -ireplace $config['url_extension'], '#{url_domain}'}|
        Set-Content -Path .env
(Get-Content -Path .env) |
    ForEach-Object {$_ -ireplace [regex]::escape($config['auth_client_secret']), '#{AuthServer_ClientSecret}'} |
        Set-Content -Path .env
