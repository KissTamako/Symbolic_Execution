(set-logic ALL)
; Executed Path ID: 7f0f306a964c316a
; Generated at: 2026-04-17 03:12:42
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const i Int)

; ((== i 0)) (False)
(assert (not (= i 0)))

(check-sat)
(get-model)
