#!/usr/bin/python
# album
# albumartist
# artist
# artwork
# comment
# compilation
# composer
# discnumber
# genre
# lyrics
# totaldiscs
# totaltracks
# tracknumber
# tracktitle
# year
# isrc
# #bitrate (read only)
# #codec (read only)
# #length (read only)
# #channels (read only)
# #bitspersample (read only)
# #samplerate (read only)

import os
import re
import csv
import music_tag


def load(path):
  with open(path) as file:
    reader = csv.DictReader(file)
    table = []
    for row in reader:
      table.append(row)
    return (table, reader.fieldnames)


def save(path, table, fieldnames):
  with open(path, 'w') as file:
    writer = csv.DictWriter(file, extrasaction='ignore',
                            fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(table)


def try_rename(old, new, ext):
  try:
    os.rename(old + ext, new + ext)
  except IOError as e:
    return e


def sync_col_a(table):
  for path in os.listdir():
    path_match = re.match(r'(\d\d\d\ - .*)\.opus', path)
    if path_match:
      meta = music_tag.load_file(path)
      track = meta['tracknumber']
      if track and str(meta['album']) == 'LaTale BGM A':
        track = int(track)
        # while len(table) < track:
        #   table.append({})
        row = table[track - 1]

        title1 = str(row['title_sc'] or row['title_en']
                     or row['title_jp'] or row['title_kr'])
        title2 = str(row['title_en'] or row['title_sc'])

        # title = title1
        # if title2 and title2 != title:
        #   title2_match = re.match(r'(.*) \(.*\)$', title2)
        #   if title2_match:
        #     title2 = title2_match.group(1)

        #     title1_match = re.match(r'(.*) (\(.*\))$', title1)
        #     if title1_match:
        #       if title1_match.group(1) == title #TODO

        title = "{} ({})".format(
          title1, title2) if title2 and title2 != title1 and not title1.endswith(')') else title1

        place1 = str(row['place_sc'] or row['place_en']
                     or row['place_jp'] or row['place_kr'])
        # place2 = str(row['place_en'])
        # place = "{} ({})".format(place1, place2) if place2 and place2 != place1 else place1
        place = place1
        name = "[{}] {}".format(place, title)
        artist = row['artist'] or 'LaTale'
        meta['title'] = name
        # meta['album'] = "LaTale BGM A"
        meta['artist'] = artist
        # meta['tracknumber'] = track
        meta.save()
        old_path = path_match.group(1)
        new_path = "{:0>3d} - {} - {}".format(track, artist, name)
        try_rename(old_path, new_path, ".opus")
        try_rename(old_path, new_path, ".webp")
        try_rename(old_path, new_path, ".jpg")


def sync_col_b(table):
  for path in os.listdir():
    path_match = re.match(r'(B\d\d - .*)\.opus', path)
    if path_match:
      meta = music_tag.load_file(path)
      track = meta['tracknumber']
      if track and str(meta['album']) == 'LaTale BGM B':
        track = int(track)
        # while len(table) < track:
        #   table.append({})
        row = table[track - 1]
        title = row['title_en'] or row['title_kr']
        place = row['place_en'] or row['place_kr']
        name = "[{}]".format(place)
        if title:
          name += " " + title
        artist = 'LaTale'
        meta['title'] = name
        # meta['album'] = 'LaTale BGM B'
        meta['artist'] = artist
        # meta['tracknumber'] = track
        meta.save()
        old_path = path_match.group(1)
        new_path = "B{:0>2d}. {} - {}".format(track, artist, name)
        try_rename(old_path, new_path, ".opus")
        try_rename(old_path, new_path, ".webp")
        try_rename(old_path, new_path, ".jpg")


def create_col_b(table):
  for path in os.listdir():
    path_match = re.match(r'B\d\d\. LaTale - \[(.+)\]( .+)?\.opus', path)
    if path_match:
      print(path_match.groups())
      meta = music_tag.load_file(path)
      track = int(meta['tracknumber'])
      while len(table) < track:
        table.append({})
      row = table[track - 1]
      row['title_en'] = path_match.group(
        2).strip() if path_match.group(2) else ''
      row['place_en'] = path_match.group(1)


def main_a():
  table, fieldnames = load('col_a.csv')
  sync_col_a(table)
  save('~col_a.csv', table, fieldnames)
  os.rename('~col_a.csv', 'col_a.csv')


def main_b():
  table, fieldnames = load('col_b.csv')
  sync_col_b(table)
  save('~col_b.csv', table, fieldnames)
  os.rename('~col_b.csv', 'col_b.csv')


if __name__ == '__main__':
  main_a()
  main_b()
