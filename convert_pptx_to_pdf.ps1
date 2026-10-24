$pptxPath = Resolve-Path "slides\Assignment2_Regularization_MNIST_Frans_Alwan_Purba.pptx"
$pdfPath = [System.IO.Path]::ChangeExtension($pptxPath, ".pdf")

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $presentation = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    $presentation.SaveAs($pdfPath, 32)
    $presentation.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    Write-Host "SUCCESS: $pdfPath"
} catch {
    Write-Host "ERROR: $_"
}
