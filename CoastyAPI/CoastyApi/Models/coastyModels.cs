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
}