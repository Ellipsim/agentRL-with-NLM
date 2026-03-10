#!/bin/bash
# =============================================================================
# Generate blocksworld problems for train/val/test with configurable options
# Usage:
#   bash generate_problems.sh [--train N MIN MAX] [--val N MIN MAX] [--test N MIN MAX]
# Example:
#   bash generate_problems.sh --train 100 2 6 --val 50 2 6 --test 50 2 8
# =============================================================================

# Directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Project root is agentRL
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Generator location
GENERATOR="${PROJECT_ROOT}/problem_generator/pddl-generators/blocksworld/blocksworld"

# Output directory for generated problems
DATA_DIR="${PROJECT_ROOT}/data/problems"

# Default configuration
TRAIN_COUNT=100
TRAIN_MIN_BLOCKS=2
TRAIN_MAX_BLOCKS=6

VAL_COUNT=50
VAL_MIN_BLOCKS=2
VAL_MAX_BLOCKS=6

TEST_COUNT=50
TEST_MIN_BLOCKS=2
TEST_MAX_BLOCKS=8

# ---------------------------
# Help message
# ---------------------------
print_help() {
    cat << EOF
Usage: bash generate_problems.sh [options]

Options:
  --train <count> <min_blocks> <max_blocks>   Generate training problems
  --val   <count> <min_blocks> <max_blocks>   Generate validation problems
  --test  <count> <min_blocks> <max_blocks>   Generate test problems
  --help                                      Show this help message and exit

Example:
  bash generate_problems.sh --train 200 2 6 --val 50 2 5 --test 50 3 8
EOF
}

# ---------------------------
# Parse command-line arguments
# ---------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --train)
            TRAIN_COUNT=$2
            TRAIN_MIN_BLOCKS=$3
            TRAIN_MAX_BLOCKS=$4
            shift 4
            ;;
        --val)
            VAL_COUNT=$2
            VAL_MIN_BLOCKS=$3
            VAL_MAX_BLOCKS=$4
            shift 4
            ;;
        --test)
            TEST_COUNT=$2
            TEST_MIN_BLOCKS=$3
            TEST_MAX_BLOCKS=$4
            shift 4
            ;;
        --help)
            print_help
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            print_help
            exit 1
            ;;
    esac
done

# Verify generator exists
if [ ! -f "${GENERATOR}" ]; then
    echo "ERROR: Generator not found at ${GENERATOR}"
    echo "Make sure problem_generator is built"
    exit 1
fi

# Safety check: existing problems
if [ -d "${DATA_DIR}" ]; then
    echo "Existing problem folders detected in ${DATA_DIR}:"
    ls -1 "${DATA_DIR}"
    echo ""
    read -p "Erase all existing problems and generate new ones? (y/N): " CONFIRM
    CONFIRM=${CONFIRM,,}
    if [[ "$CONFIRM" == "y" || "$CONFIRM" == "yes" ]]; then
        echo "Erasing old problems..."
        rm -rf "${DATA_DIR}"/*
    else
        echo "Skipping problem removal. New problems may overwrite existing ones."
    fi
fi

# Ensure train/val/test directories exist
mkdir -p "${DATA_DIR}/train" "${DATA_DIR}/val" "${DATA_DIR}/test"

SEED=0

# ---------------------------
# Helper function to generate problems
# ---------------------------
generate_problems() {
    local COUNT=$1
    local MIN_BLOCKS=$2
    local MAX_BLOCKS=$3
    local OUT_DIR=$4
    local NAME=$5

    echo "Generating $NAME problems: $COUNT problems, blocks $MIN_BLOCKS-$MAX_BLOCKS"

    for i in $(seq 1 "$COUNT"); do
        BLOCKS=$(( (RANDOM % (MAX_BLOCKS - MIN_BLOCKS + 1)) + MIN_BLOCKS ))
        SEED=$((SEED + 1))
        "${GENERATOR}" 4 ${BLOCKS} ${SEED} > "${OUT_DIR}/problem_${i}.pddl"
    done
}

# ---------------------------
# Generate datasets
# ---------------------------
generate_problems "$TRAIN_COUNT" "$TRAIN_MIN_BLOCKS" "$TRAIN_MAX_BLOCKS" "${DATA_DIR}/train" "Training"
generate_problems "$VAL_COUNT" "$VAL_MIN_BLOCKS" "$VAL_MAX_BLOCKS" "${DATA_DIR}/val" "Validation"
generate_problems "$TEST_COUNT" "$TEST_MIN_BLOCKS" "$TEST_MAX_BLOCKS" "${DATA_DIR}/test" "Test"

# ---------------------------
# Summary
# ---------------------------
echo ""
echo "Done! Generated:"
echo "  Train: $(ls "${DATA_DIR}/train/"*.pddl 2>/dev/null | wc -l) problems"
echo "  Val:   $(ls "${DATA_DIR}/val/"*.pddl 2>/dev/null | wc -l) problems"
echo "  Test:  $(ls "${DATA_DIR}/test/"*.pddl 2>/dev/null | wc -l) problems"
echo ""
echo "Output directory: ${DATA_DIR}"