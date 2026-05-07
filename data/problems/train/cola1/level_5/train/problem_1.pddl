

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b5)
(ontable b4)
(ontable b5)
(on b6 b3)
(on b7 b1)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b3 b4)
(on b5 b7)
(on b6 b3)
(on b7 b2))
)
)


