#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Uso: $0 nome_do_arquivo"
    exit 1
fi

arquivo=$1

sed -i 's/ \+/ /g' "$arquivo"

sed -i 's/^[ \t]*//;s/[ \t]*$//' "$arquivo"

sed -i 's/\r$//' "$arquivo"

echo "Arquivo $arquivo limpo com sucesso"
