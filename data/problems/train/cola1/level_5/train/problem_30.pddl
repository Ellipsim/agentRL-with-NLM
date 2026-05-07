

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b6)
(ontable b3)
(on b4 b5)
(on b5 b1)
(ontable b6)
(on b7 b3)
(clear b2)
(clear b4)
)
(:goal
(and
(on b1 b6)
(on b3 b4)
(on b4 b1)
(on b5 b7)
(on b7 b2))
)
)


