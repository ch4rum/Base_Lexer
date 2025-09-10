#!/usr/bin/env bash
#   ┏┓ ┏━┓┏━┓┏━╸   ╻  ┏━╸╻ ╻┏━╸┏━┓
#   ┣┻┓┣━┫┗━┓┣╸    ┃  ┣╸ ┏╋┛┣╸ ┣┳┛
#   ┗━┛╹ ╹┗━┛┗━╸   ┗━╸┗━╸╹ ╹┗━╸╹┗╸
#	Author	-	ch4rum
#	Repo	-	https://github.com/ch4rum/Base_Lexer
#	Installer - Script to install requeriment
#
# Copyright (C) 2025 ch4rum

# Colors
CRE=$(tput setaf 1)    # Red
CYE=$(tput setaf 3)    # Yellow
CGR=$(tput setaf 2)    # Green
CBL=$(tput setaf 4)    # Blue
BLD=$(tput bold)       # Bold
CNC=$(tput sgr0)       # Reset colors

# ---------- Gobal Variables ----------
ERROR_LOG="$PWD/Ch4rumLexer.log"
PKG_MANAGER=""
DISTRO=""

# ---------- Functions ----------
logo(){
    text="$1"
    printf "%b" "
    ${CBL}┏┓ ┏━┓┏━┓┏━╸${CYE}   ╻  ${CGR}┏━╸╻ ╻${CMA}┏━╸┏━┓
    ${CBL}┣┻┓┣━┫┗━┓${CYE}┣╸    ┃  ${GYE}┣╸ ┏╋┛${CMA}┣╸ ┣┳┛
    ${CBL}┗━┛╹ ╹┗━┛${CYE}┗━╸   ┗━╸${GYE}┗━╸╹ ╹${CMA}┗━╸╹┗╸
    \t\t${BLD}${CRE}[ ${CYE}${text} ${CRE}]${CNC}\n\n"
}

log_error() {
    local error_msg=$1
    local timestamp
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    printf "%s\n" "[${timestamp}] ERROR: ${error_msg}" >> "$ERROR_LOG"
    printf "%s%s[ERROR]:%s %s\n" "${CRE}" "${BLD}" "${CNC}" "${error_msg}" >&2
}

welcome() {
    clear
    logo "Welcome $USER"
    sleep 2
    printf "%b\n" "${BLD}${CGR}This script will set up your Python Lexer environment.${CNC}"
    printf "%b\n" "${BLD}${CGR}Here's what it will do:${CNC}\n"
    printf "  ${BLD}${CGR}[${CYE}i${CGR}]${CNC} Detect your Linux distribution (Arch, Ubuntu, etc)\n"
    printf "  ${BLD}${CGR}[${CYE}i${CGR}]${CNC} Check for required system packages and install them if missing\n"
    printf "  ${BLD}${CGR}[${CYE}i${CGR}]${CNC} Create a Python virtual environment (.lexer)\n"
    printf "  ${BLD}${CGR}[${CYE}i${CGR}]${CNC} Activate the virtual environment and install pip dependencies\n"
    printf "  ${BLD}${CGR}[${CYE}i${CGR}]${CNC} Optionally install from requirements.txt if found\n"
    printf "\n"
    printf "  ${BLD}${CGR}[${CRE}!${CGR}]${CNC} ${BLD}${CRE}This script does NOT modify system configurations or user files${CNC}\n"
    printf "  ${BLD}${CGR}[${CRE}!${CGR}]${CNC} ${BLD}${CRE}Safe to run multiple times — will skip already installed packages${CNC}\n"
    printf "\n"
    while :; do
        printf "%b" "${BLD}${CGR}Do you wish to continue?${CNC} [y/N]: "
        read -r yn < /dev/tty
        case "$yn" in 
            [Yy])
                detect_distro
                break ;;
            [Nn] | "") 
                printf "\n%b\n" "${BLD}${CYE}Operation cancelled.${CNC}\n"
                exit 0 ;;
            *)
                printf "\n%b\n" "${BLD}${CRE}Error:${CNC} Please type '${BLD}${CYE}y${CNC}' or '${BLD}${CYE}n${CNC}'\n" ;;
        esac
    done
}

detect_distro() {
    if [ -f /etc/os-release ]; then
        source /etc/os-release
        DISTRO=$ID
    fi
    case "$DISTRO" in
        arch | manjaro)
            PKG_MANAGER="pacman"
            ;;
        debian | ubuntu | linuxmint)
            PKG_MANAGER="apt"
            ;;
        *)
            log_error "Unsupported or unknown distro: $DISTRO"
            exit 1
            ;;
    esac
}

install_system_package() {
    local pkg=$1
    case "$PKG_MANAGER" in
        pacman)
            if ! pacman -Qq "$pkg" &>/dev/null; then
                printf "%b\n" "${BLD}${CGR}[+]${CNC} ${BLD}${CBL}Installing ${CYE}$pkg${CNC}${BLD}${CBL} with pacman.${CNC}"
                if ! sudo pacman -S --noconfirm "$pkg" 2>>"$ERROR_LOG"; then
                    log_error "Failed to install $pkg with pacman"
                fi
            else
                printf "%b\n" "${BLD}${CGR}[✓]${CNC} ${BLD}${CYE}${pkg}${CNC}${BLD}${CBL} is already installed.${CNC}"
            fi
            ;;
        apt)
            if ! dpkg -l | grep -qw "$pkg"; then
                printf "%b\n" "${BLD}${CGR}[+]${CNC} ${BLD}${CBL}Installing ${CYE}$pkg${CNC}${BLD}${CBL} with apt.${CNC}"
                if ! sudo apt update && sudo apt install -y "$pkg" 2>>"$ERROR_LOG"; then
                    log_error "Failed to install $pkg with apt"
                fi
            else
                printf "%b\n" "${BLD}${CGR}[✓]${CNC} ${BLD}${CYE}${pkg}${CNC}${BLD}${CBL} is already installed.${CNC}"
            fi
            ;;
    esac
}

setup_system_requirements() {
    sleep 2
    clear
    logo "Installing necessary packages..."
    sleep 2
    local packages=""
    case "$PKG_MANAGER" in
        pacman)
            packages="python python-pip tk git"
            ;;
        apt)
            packages="python3 python3-pip python3-venv python3-tk git"
            ;;
    esac
    for pkg in $packages; do
        install_system_package "$pkg"
        sleep 2
    done
}

clone_repo() {
    sleep 2
    clear
    logo "Downloading repository"
    sleep 2
    if [ -d ".git" ] || [ -d ".lexer" ] || [ -f "README.md" ]; then
        printf "%b\n" "${BLD}${CGR}[✓]${CNC}${BLD}${CBL} Detected existing ${CNC}${BLD}${CYE}Base-Lexer${CNC}${BLD}${CBL} repository in current directory.${CNC}"
        return 0
    fi
    if [ ! -d "Base_Lexer" ]; then
        printf "%b\n" "${BLD}${CGR}[+]${CNC}${BLD}${CBL} Cloning ${BLD}${CYE}Base-Lexer${CNC}${BLD}${CBL} repository...${CNC}"
        if ! git clone https://github.com/ch4rum/Base_Lexer.git 2>>"$ERROR_LOG"; then
            log_error "Failed to clone Base-Lexer repository"
            exit 1
        else
            printf "%b\n" "${BLD}${CGR}[✓]${CNC}${BLD}${CBL} Repository cloned successfully.${CNC}"
        fi
    else
        printf "%b\n" "${BLD}${CGR}[✓]${CNC} ${BLD}${CYE}Base-Lexer${CNC}${BLD}${CBL} repository already cloned.${CNC}"
    fi
}

install_python_dependencies() {
    sleep 2
    clear
    logo "Installing dependencies... "
    sleep 2
    local dependencies="customtkinter ply"
    if [ -d "Base_Lexer" ]; then
        cd Base_Lexer || exit 1
    fi
    if [ ! -d ".lexer" ]; then
        printf "%b\n" "${BLD}${CGR}[+]${CNC} ${BLD}${CBL}Creating virtual environment...${CNC}"
        if ! python3 -m venv .lexer 2>>"$ERROR_LOG"; then
            log_error "Failed to create virtual environment"
            return 1
        fi
    fi
    if [ ! -f ".lexer/bin/activate" ]; then
        log_error "Virtual environment not found or activate script missing"
        return 1
    fi
    source .lexer/bin/activate
    if ! command -v pip &>/dev/null; then
        log_error "pip not found in virtual environment"
        return 1
    fi
    for pkg in $dependencies; do
        if pip show "$pkg" &>/dev/null; then
            printf "%b\n" "${BLD}${CGR}[✓]${CNC} ${BLD}${CYE}${pkg}${CNC} ${BLD}${CBL}is already installed.${CNC}"
        else
            printf "%b\n" "${BLD}${CGR}[+]${CNC} ${BLD}${CBL}Installing ${BLD}${CYE}${pkg}${CNC}${BLD}${CBL}...${CNC}"
            if ! pip install "$pkg" 2>>"$ERROR_LOG"; then
                log_error "Failed to install $pkg with pip"
            fi
        fi
    done
    #if [ -f "requirements.txt" ]; then
    #    printf "%b\n" "${BLD}${CGR}[+]${CNC} ${BLD}${CBL}Installing from requirements.txt...${CNC}"
    #    if ! pip install -r requirements.txt 2>>"$ERROR_LOG"; then
    #        log_error "Failed to install from requirements.txt"
    #    fi
    #else
    #    log_error "requirements.txt not found"
    #fi
}

all_done(){
    sleep 2
    clear
    logo "Installation complete!"
    sleep 2
    printf "%b\n" "${BLD}${CGR}Installation completed successfully!${CNC}"
    printf "%b\n" "To activate the virtual environment, run:"
    printf "%b\n\n" "${CBL} source .lexer/bin/activate${CNC}"
}

# ---------- Main Run ----------
welcome
setup_system_requirements
clone_repo
install_python_dependencies
all_done
