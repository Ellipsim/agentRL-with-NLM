

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b7)
(ontable b3)
(on b4 b6)
(ontable b5)
(ontable b6)
(on b7 b5)
(clear b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b6)
(on b5 b4))
)
)


