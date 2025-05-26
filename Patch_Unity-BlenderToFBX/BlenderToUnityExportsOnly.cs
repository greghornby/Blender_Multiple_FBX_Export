using UnityEditor;
using UnityEngine;

public class BlenderToUnityExportsOnly : AssetPostprocessor {
  void OnPostprocessModel(GameObject g) {
    StripTaggedObjects(g.transform);
  }

  void StripTaggedObjects(Transform root)
  {
    var toRemove = new System.Collections.Generic.List<GameObject>();

    foreach (Transform child in root.GetComponentsInChildren<Transform>(true))
    {
      if (child.name.StartsWith("UnityDestroy__"))
        toRemove.Add(child.gameObject);
    }

    foreach (var obj in toRemove)
      Object.DestroyImmediate(obj);
  }
}
