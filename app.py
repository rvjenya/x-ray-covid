import streamlit as st
from torchvision import models, transforms
import torch
from PIL import Image
from PIL import Image

@st.cache(allow_output_mutation=True)
def predict(image_path):
    finmodel = torch.load('covid_resnet18_epoch500.pt', map_location=torch.device('cpu'))

    transform = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    img = Image.open(image_path)
    batch_t = torch.unsqueeze(transform(img), 0)

    finmodel.eval()
    out = finmodel(batch_t)

    with open('classes.txt') as f:
        classes = [line.strip() for line in f.readlines()]

    prob = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    return [(classes[idx], prob[idx].item()) for idx in indices[0][:5]]

st.set_option('deprecation.showfileUploaderEncoding', False)

st.title("X-Ray Covid-19 Classification App")
st.write("")
video_file = open('image/start-demo-x-ray-classify.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)
st.subheader("Two sources are used to create this dataset: ")
st.write("Covid-Chestxray-Dataset, for COVID-19 X-ray samples")
st.write("ChexPert Dataset, for Non-COVID samples")

file_up = st.file_uploader("Please Upload an image of X-Ray", type=["jpg", "png", "jpeg"])

if file_up is not None:
    image = Image.open(file_up)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Just a second...")
    labels = predict(file_up)

    # print out the top 5 prediction labels with scores
    for i in labels:
        st.write("Prediction (index, name)", i[0], ",   Score: ", i[1], "%")