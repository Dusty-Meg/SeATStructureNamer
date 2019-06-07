using System;

namespace SeATStructureNamer
{
    public class RefreshTokens
    {
        public long character_id { get; set; }
        public string refresh_token { get; set; }
        public DateTime expires_on { get; set; }
        public string token { get; set; }
        public DateTime? deleted_at { get; set; }

        public virtual CharacterInfo User { get; set; }
    }
}