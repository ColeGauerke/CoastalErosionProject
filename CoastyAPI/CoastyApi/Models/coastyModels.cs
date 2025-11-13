using Newtonsoft.Json;

namespace CoastyApi.Models
{
    public class User
    {
        public string? name { get; set; }
    }

    public class WaterLvlRequest
    {
        public string? startDate { get; set; }
        public string? endDate { get; set; }
        public string city { get; set; }
        public string state { get; set; }
        public string period { get; set; }
    }

    public class RiskRequest
    {
        public string city { get; set; }
        public int year { get; set; }
    }

    public class NewsRequest
    {
        public bool everything { get; set; }
        public string keyword1 { get; set; }
        public string keyword2 { get; set; }
    }
}