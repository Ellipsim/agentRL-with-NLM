

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(on b4 b1)
(on b5 b3)
(ontable b6)
(on b7 b2)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b2 b4)
(on b3 b6)
(on b4 b3)
(on b6 b7)
(on b7 b5))
)
)


