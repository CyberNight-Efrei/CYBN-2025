#!/usr/bin/env bash
set -euo pipefail

# ----------------------
# Couleurs
# ----------------------
RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# ----------------------
# Valeurs par défaut
# ----------------------
ROOT="."
FILENAME="challenge.yml"
ACTION=""
CONTINUE_ON_ERROR=1   # par défaut : continuer même si une erreur survient
# ----------------------

# ----------------------
# Aide / usage
# ----------------------
usage() {
    echo -e "${YELLOW}Usage: $0 <action> [root]${NC}"
    echo
    echo "Action obligatoire :"
    echo "  add       Ajouter le challenge"
    echo "  install   Installer le challenge"
    echo "  sync      Synchroniser le challenge"
    echo "  mirror    Mirror le challenge"
    echo
    echo "root : répertoire racine pour la recherche (défaut: .)"
}

# ----------------------
# Parsing des arguments
# ----------------------
if [[ $# -lt 1 ]]; then
    echo -e "${RED}Erreur : il faut spécifier une action.${NC}"
    usage
    exit 1
fi

ACTION="$1"
shift

case "$ACTION" in
    add|install|sync|mirror)
        ;;
    *)
        echo -e "${RED}Action invalide : $ACTION${NC}"
        usage
        exit 1
        ;;
esac

# Si un root est passé en argument
if [[ $# -ge 1 ]]; then
    ROOT="$1"
fi

# ----------------------
# Recherche des fichiers
# ----------------------
mapfile -d '' -t files < <(find "$ROOT" -type f -name "$FILENAME" -print0)

if [ "${#files[@]}" -eq 0 ]; then
    echo -e "${RED}Aucun fichier '$FILENAME' trouvé sous '$ROOT'.${NC}"
    exit 1
fi

if [[ -f "$ROOT/venv/bin/activate" ]]; then

    echo -e "${YELLOW}Activation de l'environnement virtuel : $ROOT/venv/bin/activate${NC}"
    source "$ROOT/venv/bin/activate"

else

    echo -e "${RED}Pas d'environnement virtuel trouvé. Abandon.${NC}"
    exit 1

fi


# ----------------------
# Exécution de l'action
# ----------------------
for file in "${files[@]}"; do
    dir="$(dirname "$file")"
    echo -e "\n${BLUE}---------- $dir ----------${NC}"

    echo -e "${YELLOW}Exécution : ctf challenge $ACTION $dir${NC}"
    if ctf challenge "$ACTION" "$dir"; then
        echo -e "${GREEN}OK : $dir${NC}"
    else
        echo -e "${RED}ÉCHEC : $dir${NC}"
        if [ "$CONTINUE_ON_ERROR" -eq 0 ]; then
            exit 1
        fi
    fi
done

echo -e "\n${BLUE}Traitement terminé pour ${#files[@]} dossier(s).${NC}"
