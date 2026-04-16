(set-logic ALL)
; Constraint ID: f88c189b5d4a2dcc
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60517)) (False)
(assert (not (= x 60517)))

; Query: ((== x 60518)) (False)
(assert (not (not (= x 60518))))

(check-sat)
(get-model)
