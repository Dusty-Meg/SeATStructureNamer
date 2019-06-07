namespace SeATStructureNamer
{
    public class CharacterInfo
    {
        public long character_id { get; set; }
        public long corporation_id { get; set; }

        public virtual RefreshTokens RefreshToken { get; set; }
    }
}
