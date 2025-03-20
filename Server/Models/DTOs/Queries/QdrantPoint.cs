namespace Server.Models.DTOs.Queries;

public class QdrantPoint
{
	public int Id { get; set; }
	public float[] Vector { get; set; }
	public Dictionary<string, string> Payload { get; set; }
}
