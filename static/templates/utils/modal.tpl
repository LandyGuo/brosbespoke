<div class="bb-m-dia">
    <% if(title) { %><div class="bb-m-h"><%- title %></div><% } %>
    <div class="<% if(title) { %>bb-m-c<% } else { %>bb-m-d<% } %>">
        <%= content %>
    </div>
    <% if (cancelText) { %>
    <div class="bb-m-btns">
        <% if(!submitText) { %>
        <button class="bb-btn-one"><%- cancelText %></button>
        <% } else { %>
        <button class="bb-cnl"><%- cancelText %></button>
        <button class="bb-sbt"><%- submitText %></button>
        <% } %>
        <div class="clearfix"></div>
    </div>
    <% } %>
</div>