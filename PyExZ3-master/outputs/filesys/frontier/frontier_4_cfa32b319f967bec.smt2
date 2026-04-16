(set-logic ALL)
; Constraint ID: cfa32b319f967bec
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60517)) (False)
(assert (not (not (= x 60517))))

(check-sat)
(get-model)
