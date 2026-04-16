(set-logic ALL)
; Executed Path ID: b98a0d1e2f60794a
; Generated at: 2026-04-17 03:12:54
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const i Int)

; ((> (+ (* 3 (// i 100)) 100) 43)) (False)
(assert (not (> (+ (* 3 (// i 100)) 100) 43)))

(check-sat)
(get-model)
