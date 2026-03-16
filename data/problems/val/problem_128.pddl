

(define (problem BW-rand-7)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b7)
(ontable b4)
(ontable b5)
(ontable b6)
(on b7 b5)
(clear b1)
(clear b2)
(clear b3)
(clear b6)
)
(:goal
(and
(on b1 b6)
(on b2 b7)
(on b4 b3)
(on b5 b2)
(on b7 b1))
)
)


