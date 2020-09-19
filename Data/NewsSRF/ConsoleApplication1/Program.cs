using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Permissions;
using System.Text;
using System.Threading;

namespace ConsoleApplication1
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            //HardCoded data from SRF (ParallelExecutionMode 2GB)
            string path = @"C:\Users\Jann\Downloads\download\hackzurich\SMD\data_export";
            string pathWordList = @"C:\Users\Jann\Downloads\download\hackzurich\wordlists\viruswordlist.en.txt";
            // Hackaton Timeslott
            var MINDATE = DateTime.Parse("2020-03-16");
            var MAXDATE = DateTime.Parse("2020-03-30");
            var lData =new List<InData>();
            var listOutput = new List<string>();
            // Extract the data from the 100 CSV files and select the relevant time slott
            var lFiles = new DirectoryInfo(path).GetFiles();
            foreach (var file in lFiles)
            {
                if (file.Extension == ".csv")
                {
                    var lines = File.ReadAllLines(file.FullName,new UTF8Encoding(true));
                    var i = 0;
                    foreach (var line in lines)
                    {
                        i++;
                        var parts = line.Split(',');

                        if (parts.Length>9&&!string.IsNullOrWhiteSpace(parts[2])&&i>1 && DateTime.TryParse(parts[2], out var a))
                        {
                            try
                            {
                              
                                if (a > MINDATE && a<MAXDATE)
                                {
                                    var temp = new InData();
                                    temp.so = string.IsNullOrWhiteSpace(parts[0]) ? " " : parts[0];
                                    temp.Date = a;
                                    temp.Titel = string.IsNullOrWhiteSpace(parts[5]) ? " " : parts[5];
                                    temp.SubTitel = string.IsNullOrWhiteSpace(parts[7]) ? " " : parts[7];
                                    temp.rubrik = string.IsNullOrEmpty(parts[8]) ? " " : parts[8];
                                    temp.Text = string.IsNullOrWhiteSpace(parts[10]) ? " " : parts[10];
                                    lData.Add(temp);
                                }
                            }
                            catch (Exception e)
                            {
                                Console.WriteLine(e);
                                
                            }
                           
                        }
                       
                    }
                    
                }
            }
            var wordListin = File.ReadAllLines(pathWordList,new UTF8Encoding(true));
            var wordListout = new List<string>();
            foreach (var word in wordListin)
            {
             var   a = word.ToUpper();
             wordListout.Add(a);
            }
            // Check if Corona is in the news Artikle
            foreach (var data in lData)
            {
                data.isRelevant = false;
                data.isLausane = false;
                data.isGenf = false;
                data.isZurich = false;
                foreach (var word in wordListout)
                {
                    if (data.Text.ToUpper().Contains(word) || data.SubTitel.ToUpper().Contains(word) ||
                        data.Titel.ToUpper().Contains(word))
                    {
                        data.isRelevant = true;
                        break;
                    }

                }
                
                if (data.rubrik.ToUpper().Contains("ZÜRICH")||data.Text.ToUpper().Contains("ZÜRICH")||data.Text.ToUpper().Contains("ZURICH"))
                {
                    data.isZurich = true;
                }

                if (data.Text.ToUpper().Contains("LAUSANNE")||data.rubrik.ToUpper().Contains("LAUSANNE"))
                {
                    data.isLausane = true;
                }
                if (data.Text.ToUpper().Contains("GENF")||data.Text.ToUpper().Contains("GENEVA")||data.Text.ToUpper().Contains("GENEVA") ||data.Text.ToUpper().Contains("GENF") )
                {
                    data.isGenf = true;
                }
                
            }
            // Writte the CSV file
            string titel =
                "Day,All,AllRelevant,AllZurich,AllZHrelevant,AllGenf,AllGenfRelevant,AllLausane,AllLausneRelevant";
            listOutput.Add(titel);
            var resGrupDays = lData.GroupBy(e => e.Date.Day);
            foreach (var VARIABLE in resGrupDays)
            {

                string temp = VARIABLE.Key+","+VARIABLE.Count()+",";
                var b = VARIABLE.Count(y => y.isRelevant);
                temp += b + ",";
                var c = VARIABLE.Count(y => y.isZurich);
               
                var d = VARIABLE.Count(y => (y.isZurich && y.isRelevant));
                var e = VARIABLE.Count(y => y.isLausane);
                var f = VARIABLE.Count(y => y.isLausane && y.isRelevant);
                var g=VARIABLE.Count(y => y.isGenf);
                var h = VARIABLE.Count(y => y.isGenf && y.isRelevant);

                temp += c + ","+d+ ","+ ","+e+ ","+f+ ","+g+ ","+h;
                listOutput.Add(temp);

            }
                
            File.WriteAllLines("outputData_2.csv",listOutput,new UTF8Encoding(true));

        }

         class InData
        {
             public string so { get; set; }
             public string Titel { get; set; }
             public  string SubTitel { get; set; }
             public  string Text { get; set; }
             public  string rubrik { get; set; }
             
             public  DateTime Date{ get; set; }
             public bool isRelevant { get; set; }
             public bool isZurich { get; set; }
             public bool isGenf { get; set; }
             public bool isLausane { get; set; }
        }
    }
}