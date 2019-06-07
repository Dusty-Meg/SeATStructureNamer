using System;

namespace SeATStructureNamer
{
    public class UniverseStructures
    {
        public long structure_id { get; set; }
        public string name { get; set; }
        public long? owner_id { get; set; }
        public int solar_system_id { get; set; }
        public int? type_id { get; set; }
        public double x { get; set; }
        public double y { get; set; }
        public double z { get; set; }
        public DateTime? created_at { get; set; }
        public DateTime? updated_at { get; set; }
        public int? FailedCount { get; set; }
    }
}