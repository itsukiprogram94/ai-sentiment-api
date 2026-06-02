import { afterEach, describe, expect, test } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "./App";

afterEach(() => {
  cleanup();
});

describe("App", () => {
  test("renders the main title", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: /AI Sentiment Web App/i })
    ).toBeInTheDocument();
  });

  test("renders textarea and analyze button", () => {
    render(<App />);

    expect(screen.getByLabelText(/input text/i)).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /^Analyze$/i })
    ).toBeInTheDocument();
  });

  test("renders sample input buttons", () => {
    render(<App />);

    expect(
      screen.getByRole("button", { name: /^Positive$/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /^Negative$/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /^Neutral$/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /^Not good$/i })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /^Not bad$/i })
    ).toBeInTheDocument();
  });

  test("updates textarea when a sample button is clicked", async () => {
    const user = userEvent.setup();

    render(<App />);

    const textarea = screen.getByLabelText(/input text/i);

    await user.click(screen.getByRole("button", { name: /^Not good$/i }));

    expect(textarea).toHaveValue("This is not good");
  });
});