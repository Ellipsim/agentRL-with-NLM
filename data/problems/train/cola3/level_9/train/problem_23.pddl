

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(on b3 b10)
(ontable b4)
(on b5 b4)
(on b6 b3)
(ontable b7)
(on b8 b2)
(on b9 b5)
(ontable b10)
(clear b1)
(clear b7)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b6)
(on b2 b1)
(on b5 b8)
(on b6 b10)
(on b7 b9)
(on b8 b4)
(on b9 b3))
)
)


