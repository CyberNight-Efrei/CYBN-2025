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
FILENAME="build_docker.sh"
CONTINUE_ON_ERROR=1   # par défaut : continuer même si une erreur survient
RUN_FLAG=0            # par défaut : ne pas ajouter "-r" à l’exécution
# ----------------------

# ----------------------
# Aide / usage
# ----------------------
usage() {
    echo -e "${YELLOW}Usage: $0 [options] [root] [filename]${NC}"
    echo
    echo "Options:"
    echo "  -s, --strict     Arrêter à la première erreur (par défaut : continuer)"
    echo "  -r, --run        Exécuter les scripts avec l’option -r"
    echo "  -h, --help       Afficher cette aide"
    echo
    echo "Arguments :"
    echo "  root             Répertoire racine de recherche (défaut: .)"
    echo "  filename         Nom du fichier à rechercher (défaut: build_docker.sh)"
}

# ----------------------
# Parsing des arguments
# ----------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--strict)
            CONTINUE_ON_ERROR=0
            shift
            ;;
        -r|--run)
            RUN_FLAG=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            if [[ -z "${ROOT:-}" || "$ROOT" == "." ]]; then
                ROOT="$1"
            elif [[ -z "${FILENAME:-}" || "$FILENAME" == "build_docker.sh" ]]; then
                FILENAME="$1"
            else
                echo -e "${RED}Argument inattendu : $1${NC}"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# ----------------------
# Recherche des fichiers
# ----------------------
mapfile -d '' -t files < <(find "$ROOT" -type f -name "$FILENAME" -print0)

if [ "${#files[@]}" -eq 0 ]; then
    echo -e "${RED}Aucun fichier '$FILENAME' trouvé sous '$ROOT'.${NC}"
    exit 1
fi

# ----------------------
# Exécution des scripts trouvés
# ----------------------
for file in "${files[@]}"; do
    echo
    echo -e "${BLUE}---------- $file ----------${NC}"
    dir="$(dirname "$file")"
    base="$(basename "$file")"

    pushd "$dir" > /dev/null || { echo -e "${RED}Impossible de cd dans $dir${NC}"; if [ "$CONTINUE_ON_ERROR" -eq 0 ]; then exit 1; else continue; fi; }

    # Exécution selon le flag --run
    if [ "$RUN_FLAG" -eq 1 ]; then
        echo -e "${YELLOW}Exécution : sudo bash $base -r${NC}"
        if sudo bash "./$base" -r; then
            echo -e "${GREEN}OK: $file${NC}"
        else
            echo -e "${RED}ÉCHEC: $file${NC}"
            if [ "$CONTINUE_ON_ERROR" -eq 0 ]; then popd > /dev/null; exit 1; fi
        fi
    else
        echo -e "${YELLOW}Exécution : sudo bash $base${NC}"
        if sudo bash "./$base"; then
            echo -e "${GREEN}OK: $file${NC}"
        else
            echo -e "${RED}ÉCHEC: $file${NC}"
            if [ "$CONTINUE_ON_ERROR" -eq 0 ]; then popd > /dev/null; exit 1; fi
        fi
    fi

    popd > /dev/null
done

echo -e "\n${BLUE}Traitement terminé pour ${#files[@]} fichier(s).${NC}"
