

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b7)
(ontable b3)
(on b4 b3)
(on b5 b1)
(ontable b6)
(on b7 b6)
(clear b2)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b3 b2)
(on b5 b6)
(on b7 b4))
)
)


