

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(ontable b4)
(on b5 b7)
(on b6 b1)
(on b7 b3)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b3 b6)
(on b4 b3)
(on b6 b5)
(on b7 b2))
)
)


