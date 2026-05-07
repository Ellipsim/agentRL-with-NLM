

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(on b3 b8)
(ontable b4)
(on b5 b2)
(on b6 b3)
(ontable b7)
(on b8 b4)
(ontable b9)
(on b10 b12)
(on b11 b7)
(on b12 b11)
(clear b1)
(clear b5)
(clear b6)
(clear b10)
)
(:goal
(and
(on b3 b6)
(on b4 b10)
(on b5 b11)
(on b6 b9)
(on b7 b4)
(on b8 b7)
(on b9 b8)
(on b11 b2))
)
)


