(set-logic ALL)
; Constraint ID: aa2cddaa685fca17
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59572)) (False)
(assert (not (= x 59572)))

; Query: ((== x 59573)) (False)
(assert (not (not (= x 59573))))

(check-sat)
(get-model)
