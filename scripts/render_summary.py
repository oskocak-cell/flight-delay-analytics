"""Render a dependency-free SVG overview from the reproduced airline CSV."""
import csv
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    with (ROOT/"reports/reproduced/delay_by_airline.csv").open(newline="") as handle:
        rows=list(csv.DictReader(handle))
    row_height=42; height=170+len(rows)*row_height
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">',
         '<title id="title">Flight delays in the educational sample</title>',
         '<desc id="desc">Average departure and arrival clock-time delays by airline. Sample observations only, with flight counts. These are not real airline performance estimates.</desc>',
         f'<rect width="1100" height="{height}" fill="#f7f9fc"/>',
         '<g font-family="Arial, sans-serif" fill="#172b4d">',
         '<text x="36" y="40" font-size="25" font-weight="700">Flight delay analytics</text>',
         '<text x="36" y="66" font-size="14">250 course sample flights · Clock-time rollover corrected · Minutes, including early flights</text>',
         '<rect x="660" y="26" width="14" height="14" fill="#175e91"/><text x="682" y="38" font-size="13">Departure</text>',
         '<rect x="800" y="26" width="14" height="14" fill="#27a39c"/><text x="822" y="38" font-size="13">Arrival</text>']
    for tick in range(0,31,5):
        x=300+tick*20
        svg += [f'<line x1="{x}" y1="106" x2="{x}" y2="{height-62}" stroke="#dce3ed"/>',f'<text x="{x}" y="98" font-size="12" text-anchor="middle">{tick}</text>']
    for i,row in enumerate(rows):
        y=118+i*row_height
        svg += [f'<text x="36" y="{y+16}" font-size="14">{escape(row["airline"])}</text>',f'<text x="258" y="{y+16}" font-size="12" fill="#526581" text-anchor="end">n={row["total_flights"]}</text>']
        for offset,key,color in [(0,"avg_departure_delay_min","#175e91"),(17,"avg_arrival_delay_min","#27a39c")]:
            value=float(row[key]);width=value*20
            svg += [f'<rect x="300" y="{y+offset}" width="{width:.2f}" height="13" rx="2" fill="{color}"/>',f'<text x="{310+width:.2f}" y="{y+offset+11}" font-size="11">{value:.1f}</text>']
    svg += [f'<text x="36" y="{height-24}" font-size="13" fill="#526581">Educational sample only · Small group sizes · No causal or real-world airline ranking claims</text>','</g></svg>']
    (ROOT/"docs/images/airline-delays.svg").write_text("\n".join(svg)+"\n")

if __name__=="__main__":main()
