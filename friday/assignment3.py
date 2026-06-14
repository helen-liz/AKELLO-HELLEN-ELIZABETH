"""
FIFA World Cup 2026 Simulation
Manager: Guide your national team to World Cup victory
Uses: while loop, break, continue, and pass statements
"""

import random

# Initialize team stats
class Team:
    def __init__(self):
        self.morale = 80
        self.strength = 75
        self.injuries = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.goal_diff = 0

def display_team_status(team):
    """Display current team statistics"""
    print("\n" + "="*50)
    print("TEAM STATUS")
    print("="*50)
    print(f"Morale: {team.morale}%")
    print(f"Strength: {team.strength}%")
    print(f"Injured Players: {team.injuries}")
    print(f"Record: W-{team.wins} | D-{team.draws} | L-{team.losses}")
    print(f"Goal Difference: {team.goal_diff:+d}")
    print("="*50 + "\n")

def pre_tournament_preparation(team):
    """Pre-tournament training and preparation phase"""
    print("\n" + "*"*50)
    print("PRE-TOURNAMENT PREPARATION PHASE")
    print("*"*50)
    print("\nYour team has 2 weeks before the tournament starts!")
    print("Choose how to prepare your team:\n")
    
    preparation_week = 1
    max_weeks = 2
    
    while preparation_week <= max_weeks:
        print(f"\n--- WEEK {preparation_week} ---")
        print("1. Intensive Training (↑Strength, ↓Morale)")
        print("2. Recovery & Rest (↑Morale, slight ↑Strength)")
        print("3. Friendly Match (Test formations, risk injuries)")
        print("4. Skip this week (pass - placeholder for future features)")
        
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == "1":
            print("\n🏋️ INTENSIVE TRAINING SESSION")
            team.strength = min(team.strength + 8, 100)
            team.morale = max(team.morale - 5, 0)
            print(f"Strength: +8% | Morale: -5%")
            print(f"Team ready for battle! (Strength: {team.strength}%, Morale: {team.morale}%)")
            preparation_week += 1
            
        elif choice == "2":
            print("\n🏖️ RECOVERY & REST WEEK")
            team.morale = min(team.morale + 10, 100)
            team.strength = min(team.strength + 3, 100)
            print(f"Morale: +10% | Strength: +3%")
            print(f"Team is refreshed and energized! (Morale: {team.morale}%, Strength: {team.strength}%)")
            preparation_week += 1
            
        elif choice == "3":
            print("\n⚽ FRIENDLY MATCH")
            opponent = random.choice(["Team A", "Team B", "Team C"])
            result = random.randint(1, 3)
            
            if result == 1:
                print(f"Won against {opponent} 2-1!")
                team.wins += 1
                team.morale = min(team.morale + 5, 100)
            elif result == 2:
                print(f"Drew with {opponent} 1-1")
                team.draws += 1
            else:
                print(f"Lost to {opponent} 0-1")
                team.losses += 1
                team.morale = max(team.morale - 3, 0)
                new_injuries = random.randint(1, 3)
                team.injuries += new_injuries
                print(f"⚠️ {new_injuries} players injured!")
            
            preparation_week += 1
            
        elif choice == "4":
            print("\n⏭️ Skipping this week (placeholder for future tournament features)")
            # pass statement - placeholder for future features
            pass
            preparation_week += 1
            
        else:
            print("Invalid choice! Please try again.")
            # continue to next iteration without incrementing week
            continue
        
        display_team_status(team)
    
    print("\n✅ Pre-tournament preparation complete! Tournament starts tomorrow!")
    return team

def play_match(team, opponent_name, match_type):
    """Simulate a match"""
    # Strength and morale affect performance
    performance_factor = (team.strength + team.morale) / 200
    injury_penalty = team.injuries * 0.05
    
    # Calculate team power
    team_power = performance_factor - injury_penalty
    
    # Random opponent strength
    opponent_power = random.uniform(0.6, 1.0)
    
    # Determine result
    if team_power > opponent_power + 0.1:
        result = "WIN"
        goals_for = random.randint(2, 4)
        goals_against = random.randint(0, 1)
        team.wins += 1
        team.morale = min(team.morale + 3, 100)
    elif team_power < opponent_power - 0.1:
        result = "LOSS"
        goals_for = random.randint(0, 1)
        goals_against = random.randint(2, 4)
        team.losses += 1
        team.morale = max(team.morale - 5, 0)
    else:
        result = "DRAW"
        goals_for = random.randint(1, 2)
        goals_against = random.randint(1, 2)
        team.draws += 1
        team.morale = max(team.morale - 2, 0)
    
    team.goal_diff += (goals_for - goals_against)
    
    print(f"\n🏟️  {match_type}: vs {opponent_name}")
    print(f"Final Score: Your Team {goals_for} - {goals_against} {opponent_name}")
    print(f"Result: {result}")
    
    # Random injuries risk
    if random.random() < 0.3:
        new_injuries = random.randint(1, 2)
        team.injuries += new_injuries
        print(f"⚠️ WARNING: {new_injuries} players injured!")
    
    return result

def group_stage(team):
    """Group stage - 3 matches"""
    print("\n" + "*"*50)
    print("GROUP STAGE - 3 MATCHES")
    print("*"*50)
    print("Face three group opponents. Need 2 wins or 1 win + 1 draw minimum.\n")
    
    opponents = ["Team X", "Team Y", "Team Z"]
    match_num = 0
    
    while match_num < 3:
        match_num += 1
        print(f"\n--- MATCH {match_num} ---")
        
        # Check team status before match
        if team.strength < 30:
            print("⚠️ Your team is too weak! Automatic loss this match. (continue)")
            team.losses += 1
            # continue statement - skip to next iteration
            continue
        
        if team.morale < 20:
            print("😞 Team morale is critically low. Skipping recovery...")
            print("Morale recovery +15%")
            team.morale = min(team.morale + 15, 100)
            # continue statement - restart this match after recovery
            continue
        
        result = play_match(team, opponents[match_num - 1], f"Group Match {match_num}")
        display_team_status(team)
    
    # Check if team advanced
    points = (team.wins * 3) + team.draws
    print(f"\nGroup Stage Complete! Total Points: {points}")
    
    if team.wins >= 2 or (team.wins >= 1 and team.draws >= 1):
        print("✅ ADVANCED TO KNOCKOUT STAGE!")
        return True
    else:
        print("❌ ELIMINATED from tournament")
        return False

def knockout_stage(team):
    """Knockout stages - Round of 16, QF, SF, Final"""
    print("\n" + "*"*50)
    print("KNOCKOUT STAGE")
    print("*"*50)
    
    stages = [
        ("Round of 16", "Portugal"),
        ("Quarter-Final", "Belgium"),
        ("Semi-Final", "France"),
        ("WORLD CUP FINAL", "Argentina")
    ]
    
    stage_num = 0
    
    while stage_num < len(stages):
        stage_name, opponent = stages[stage_num]
        
        print(f"\n--- {stage_name} ---")
        
        # Skip recovery option (placeholder for future feature)
        if stage_num > 0:
            recovery_choice = input(f"\nBefore {stage_name}, recovery training? (y/n): ").strip().lower()
            if recovery_choice == "y":
                team.morale = min(team.morale + 8, 100)
                team.injuries = max(team.injuries - 1, 0)
                print("Recovery complete! Team refreshed.")
            else:
                print("Skipping recovery (pass - placeholder)")
                # pass statement
                pass
        
        result = play_match(team, opponent, stage_name)
        
        if result == "LOSS":
            print(f"\n❌ Tournament ended at {stage_name}.")
            print(f"Final Record: W-{team.wins} | D-{team.draws} | L-{team.losses}")
            return False
        
        display_team_status(team)
        stage_num += 1
    
    print("\n🏆 " + "="*50)
    print("WORLD CUP CHAMPIONS! 🏆")
    print("="*50)
    print(f"Tournament Record: W-{team.wins} | D-{team.draws} | L-{team.losses}")
    print(f"Goal Difference: {team.goal_diff:+d}")
    print("Your nation celebrates the greatest victory in football history!")
    print("="*50 + "\n")
    return True

def main():
    """Main tournament simulation"""
    print("\n" + "🌍"*25)
    print("    FIFA WORLD CUP 2026 - NATIONAL TEAM MANAGER SIMULATOR")
    print("🌍"*25)
    print("\nWelcome, Coach! Your mission: Lead your nation to World Cup glory!")
    
    team = Team()
    tournament_active = True
    phase = "PREPARATION"
    
    # Main tournament loop using while statement
    while tournament_active:
        
        if phase == "PREPARATION":
            team = pre_tournament_preparation(team)
            phase = "GROUP_STAGE"
            
        elif phase == "GROUP_STAGE":
            advanced = group_stage(team)
            if not advanced:
                print("\n🔴 TOURNAMENT ENDED - GROUP STAGE ELIMINATION")
                # break statement - exit tournament loop on failure
                break
            phase = "KNOCKOUT"
            
        elif phase == "KNOCKOUT":
            won_tournament = knockout_stage(team)
            if won_tournament:
                print("\n🟢 TOURNAMENT VICTORY ACHIEVED!")
                # break statement - exit tournament loop on success
                break
            else:
                print("\n🔴 TOURNAMENT FAILED")
                # break statement - exit tournament loop
                break
    
    # Final summary
    print("\n" + "="*50)
    print("TOURNAMENT SUMMARY")
    print("="*50)
    print(f"Matches Played: {team.wins + team.draws + team.losses}")
    print(f"Wins: {team.wins} | Draws: {team.draws} | Losses: {team.losses}")
    print(f"Goal Difference: {team.goal_diff:+d}")
    print("="*50 + "\n")
    
    play_again = input("Would you like to run another tournament? (y/n): ").strip().lower()
    if play_again == "y":
        # Recursive call for another tournament
        main()
    else:
        print("\nThank you for playing! Good luck coaching your nation! 🏆\n")

if __name__ == "__main__":
    main()
