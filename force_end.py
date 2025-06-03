from midiutil import MIDIFile

# === Parametri ===
initial_number = 196
steps = 50
tempo = 160
output_midi = "lychrel_196_jazz_with_swing_drums.mid"

# === Algoritmul Reverse-and-Add ===
def reverse_and_add(n):
    return n + int(str(n)[::-1])

def generate_lychrel_digits(n, steps):
    digits = []
    for _ in range(steps):
        n = reverse_and_add(n)
        digits.extend([int(d) for d in str(n)])
    return digits

# === Mapare cifre → note MIDI ===
digit_to_note = {
    0: 48, 1: 50, 2: 52, 3: 53, 4: 55,
    5: 57, 6: 59, 7: 60, 8: 62, 9: 64
}

# === Creare fișier MIDI cu saxofon + tobe jazz ===
def create_midi_with_jazz_drums(digits, path):
    midi = MIDIFile(2)  # 2 piste: sax + tobe

    # 🎷 Pista 0 – Saxofon Jazz
    track_sax = 0
    channel_sax = 0
    midi.addTempo(track_sax, 0, tempo)
    midi.addProgramChange(track_sax, channel_sax, 0, 65)  # Alto Sax

    time = 0
    for i, digit in enumerate(digits):
        note = digit_to_note.get(digit, 60)
        duration = 0.6 if i % 2 == 0 else 0.3  # swing feel
        midi.addNote(track_sax, channel_sax, note, time, duration, 100)
        time += duration

    # 🥁 Pista 1 – Tobă jazz (channel 9)
    track_drums = 1
    channel_drums = 9  # canalul de percuție
    drum_time = 0
    while drum_time < time:
        # Ride cymbal (swing constant)
        midi.addNote(track_drums, channel_drums, 51, drum_time, 0.4, 70)
        # Snare pe contratimp
        if int(drum_time * 2) % 4 == 1:
            midi.addNote(track_drums, channel_drums, 38, drum_time, 0.2, 90)
        # Kick drum pe 1 și 3
        if int(drum_time * 2) % 8 == 0:
            midi.addNote(track_drums, channel_drums, 35, drum_time, 0.3, 100)
        drum_time += 0.5

    # Salvare fișier
    with open(path, "wb") as f:
        midi.writeFile(f)

# === EXECUTARE ===
digits = generate_lychrel_digits(initial_number, steps)
create_midi_with_jazz_drums(digits, output_midi)
print(f"✅ MIDI generat cu succes: {output_midi}")
