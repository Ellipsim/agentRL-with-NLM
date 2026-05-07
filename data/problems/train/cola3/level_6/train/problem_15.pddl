

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b5)
(ontable b2)
(ontable b3)
(ontable b4)
(on b5 b2)
(ontable b6)
(on b7 b1)
(clear b3)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b6)
(on b3 b5)
(on b4 b1)
(on b5 b7)
(on b6 b4)
(on b7 b2))
)
)


