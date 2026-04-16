(set-logic ALL)
; Constraint ID: a64e5254ec9b69c9
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59611)) (False)
(assert (not (= x 59611)))

; Query: ((== x 59612)) (False)
(assert (not (not (= x 59612))))

(check-sat)
(get-model)
